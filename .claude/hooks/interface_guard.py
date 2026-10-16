#!/usr/bin/env python3
# my-interface-native-implement: owned; declaration=permission/enforced/interface-boundary-guard+agent-native-read-grant
"""Interface boundary guard.

Realizes two Enforced Guarantees as Claude Code hooks:

* interface-boundary-guard (PreToolUse, blocking, fail closed): blocks Executor
  Module reads outside the direct-Human Agent Native Implement prompt, blocks
  every non-Human attempt to invoke Agent Native Implement, and blocks every
  direct Interface (.interface/) or Target (.target/) mutation.
* agent-native-read-grant (UserPromptSubmit, blocking, fail closed): records a
  session- and prompt-bound read grant when the Human directly submits
  /my-interface-native-implement, clears it on every other prompt, and rejects
  the invocation when the grant cannot be recorded. The grant is honoured only
  for the main thread (no agent_id), so it never transfers to a subagent.

Usage: interface_guard.py prompt|pre [--state-dir DIR]
Any internal error exits 2, which Claude Code treats as a block.
"""
import fnmatch
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile

NATIVE_IMPLEMENT = "my-interface-native-implement"
PROJECT = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
INTERFACE = os.path.join(PROJECT, ".interface")
EXECUTOR = os.path.join(INTERFACE, "executor")
TARGET = os.path.join(PROJECT, ".target")
PROTECTED_ROOTS = (INTERFACE, TARGET)
INTEGRITY_FILES = (
    os.path.join(PROJECT, ".claude", "settings.json"),
    os.path.realpath(os.path.abspath(__file__)),
)
STATE_NAME = "claude-interface-guard"

BOUNDARY = (
    "Blocked by interface-boundary-guard: {why}. The Interface (.interface/) and Target (.target/) "
    "are read-only; the Executor Module (.interface/executor/) is readable only by the main agent "
    "within the prompt of a direct Human invocation of /my-interface-native-implement, and that "
    "grant is non-transferable. Use the realized Native artifacts; if one is missing, report "
    "Runtime drift and ask the Human to run /my-interface-native-implement."
)

# A path component exactly named .interface / .target / executor (so `logic.interface`
# or `mt5_interface` never match).
RE_INTERFACE = re.compile(r"(?<![\w.-])\.interface(?![\w-])")
RE_TARGET = re.compile(r"(?<![\w.-])\.target(?![\w-])")
RE_EXECUTOR_PATH = re.compile(r"(?<![\w.-])\.interface/+(?:\./+)*executor(?![\w-])")
RE_EXECUTOR_WORD = re.compile(r"(?<![\w-])executor(?![\w-])")
GLOB_CHARS = set("*?[{")

MUTATING_ANY_ARG = {
    "rm", "rmdir", "mv", "touch", "mkdir", "truncate", "chmod", "chown", "chgrp", "shred",
    "unlink", "tee", "patch", "chattr", "setfacl",
}
MUTATING_DEST_ARG = {"cp", "rsync", "install", "ln", "scp"}
GIT_MUTATING = {"rm", "mv", "checkout", "restore", "stash", "clean", "apply", "am", "reset", "switch", "merge", "pull", "rebase", "cherry-pick", "revert"}
RECURSIVE_SEARCH = {"rg", "ag", "ack", "ugrep"}
NO_PATH_TOOLS = {
    "Agent", "Task", "TaskCreate", "TaskGet", "TaskList", "TaskUpdate", "TaskStop", "TaskOutput",
    "TodoWrite", "WebSearch", "WebFetch", "AskUserQuestion", "SendMessage", "ListAgents",
    "EnterPlanMode", "ExitPlanMode", "ToolSearch", "ScheduleWakeup", "SendFeedback",
    "ReadNotifications", "PushNotification", "CronCreate", "CronDelete", "CronList", "Monitor",
}
PATHISH_KEY = re.compile(r"path|file|dir|uri|url|cwd|root|glob|pattern|target|source|dest|code|command|script", re.I)
WRITEISH_TOOL = re.compile(r"write|edit|create|update|delete|remove|move|rename|exec|run|put|patch|publish|upload|save", re.I)


# ----------------------------------------------------------------------------- helpers

def state_file(state_dir):
    base = state_dir or os.path.join(tempfile.gettempdir(), f"{STATE_NAME}-{os.getuid()}")
    os.makedirs(base, mode=0o700, exist_ok=True)
    return os.path.join(base, hashlib.sha256(PROJECT.encode()).hexdigest()[:16] + ".json")


def load_grants(path):
    if not os.path.exists(path):
        return {}
    with open(path) as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("grant store is malformed")
    return data


def save_grants(path, grants):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    with os.fdopen(fd, "w") as fh:
        json.dump(grants, fh)
    os.replace(tmp, path)


def resolve(p, cwd):
    p = os.path.expanduser(str(p))
    if not os.path.isabs(p):
        p = os.path.join(cwd or PROJECT, p)
    return os.path.realpath(p)


def within(path, root):
    return path == root or path.startswith(root + os.sep)


def is_protected(path):
    return any(within(path, r) for r in PROTECTED_ROOTS)


def deny(why):
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": BOUNDARY.format(why=why),
        }
    }, sys.stdout)
    sys.exit(0)


def norm(text):
    return re.sub(r"/(?:\./)+", "/", re.sub(r"/{2,}", "/", text))


def mentions_executor(text, cwd):
    """Lexical: does a string reach the Executor Module (path, cd + word, glob, or cwd)?"""
    t = norm(text)
    if RE_EXECUTOR_PATH.search(t) or EXECUTOR in t:
        return True
    if RE_INTERFACE.search(t) and RE_EXECUTOR_WORD.search(t):
        return True
    rcwd = os.path.realpath(cwd or PROJECT)
    if within(rcwd, EXECUTOR):
        return True
    if within(rcwd, INTERFACE) and (RE_EXECUTOR_WORD.search(t) or any(c in t for c in "*?[")):
        return True
    # Globs that could expand into the Executor Module, e.g. `.inter*/e*` or `.interface/*`.
    for tok in re.split(r"[\s'\"=:;|&()<>`]+", t):
        if not tok or not (GLOB_CHARS & set(tok)):
            continue
        if ".i" not in tok and "interface" not in tok and "exec" not in tok:
            continue
        if glob_reaches_executor(tok if os.path.isabs(tok) else os.path.join(rcwd, tok)):
            return True
    return False


def glob_reaches_executor(pattern):
    """Could this glob expand to the Executor Module or a path inside it?"""
    ep = EXECUTOR.split("/")
    cp = os.path.normpath(pattern).split("/")
    for i, e in enumerate(ep):
        if i >= len(cp):
            return False
        if cp[i] == "**":
            return True
        if not fnmatch.fnmatchcase(e, cp[i]):
            return False
    return True


EXCLUSION_RE = re.compile(
    r"--exclude(?:-dir)?[= ]\s*['\"]?[^\s'\"]+['\"]?"
    r"|(?:-g|--glob|--iglob)[= ]\s*['\"]?![^\s'\"]+['\"]?"
    r"|(?:-not|!)\s+-(?:i?path|i?name|wholename)\s+['\"]?[^\s'\"]+['\"]?"
    r"|-(?:i?path|i?name)\s+['\"]?[^\s'\"]+['\"]?\s+-prune"
    r"|['\"]?:(?:\((?:top,)?exclude\)|!|\^)[^\s'\"]+['\"]?"
)


def split_exclusions(text):
    """Return (text without exclusion options, [exclusions that name the Executor Module or Interface])."""
    named = [m for m in EXCLUSION_RE.findall(text) if re.search(r"executor|\.interface", m)]
    return EXCLUSION_RE.sub(" ", text), named


def mentions_protected(text):
    t = norm(text)
    return bool(RE_INTERFACE.search(t) or RE_TARGET.search(t) or INTERFACE in t or TARGET in t)


def mentions_integrity(text):
    t = norm(text)
    return ("interface_guard.py" in t) or bool(re.search(r"(?<![\w.-])\.claude/+settings\.json", t)) or (
        os.path.join(PROJECT, ".claude", "settings.json") in t)


def split_segments(cmd):
    return [s for s in re.split(r"\|\||&&|[;|&\n]", cmd) if s.strip()]


def words(segment):
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return segment.split()


def strip_prefix(argv):
    """Drop env assignments and wrappers (sudo, env, command, xargs, nohup, time)."""
    out = list(argv)
    while out and (re.match(r"^\w+=", out[0]) or out[0] in {"sudo", "env", "command", "nohup", "time", "exec", "xargs", "nice", "doas"}):
        out.pop(0)
        while out and out[0].startswith("-") and len(out) > 0:
            out.pop(0)
    return out


def segment_mutates(argv, predicate):
    """Does this command segment write/remove something matching predicate(token)?"""
    argv = strip_prefix(argv)
    if not argv:
        return False
    prog = os.path.basename(argv[0])
    args = argv[1:]
    operands = [a for a in args if not a.startswith("-")]
    if prog in MUTATING_ANY_ARG:
        return any(predicate(a) for a in args)
    if prog in MUTATING_DEST_ARG:
        return bool(operands) and predicate(operands[-1]) or any(a.startswith("--target-directory") and predicate(a) for a in args) or (
            "-t" in args and args.index("-t") + 1 < len(args) and predicate(args[args.index("-t") + 1]))
    if prog == "dd":
        return any(a.startswith("of=") and predicate(a) for a in args)
    if prog in {"sed", "perl", "ruby"} and any(re.match(r"^-[a-zA-Z]*i", a) or a.startswith("--in-place") for a in args):
        return any(predicate(a) for a in args)
    if prog == "git" and operands and operands[0] in GIT_MUTATING:
        return any(predicate(a) for a in args)
    if prog == "find":
        destructive = "-delete" in args
        for i, a in enumerate(args):
            if a in {"-exec", "-execdir", "-ok", "-okdir"} and i + 1 < len(args):
                inner = os.path.basename(args[i + 1])
                rest = args[i + 2:]
                destructive |= inner in MUTATING_ANY_ARG | MUTATING_DEST_ARG or (
                    inner in {"sed", "perl", "ruby"} and any(re.match(r"^-[a-zA-Z]*i", x) for x in rest))
        if not destructive:
            return False
        roots = []
        for a in args:
            if a.startswith("-") or a.startswith("!") or a.startswith("("):
                break
            roots.append(a)
        roots = [resolve(r, FIND_CWD[0]) for r in roots] or [os.path.realpath(FIND_CWD[0])]
        excluded = any(re.search(r"\.interface|\.target", m) for m in EXCLUSION_RE.findall(" ".join(args)))
        reaches = any(predicate(r) or (not excluded and (within(INTERFACE, r) or within(TARGET, r))) for r in roots)
        return reaches or any(predicate(a) for a in args)
    return False


FIND_CWD = [PROJECT]


def redirect_targets(segment):
    return re.findall(r"(?<![0-9&<])>{1,2}\|?\s*([^\s;&|<>]+)", segment)


def bash_mutates(cmd, predicate):
    for seg in split_segments(cmd):
        if any(predicate(t) for t in redirect_targets(seg)):
            return True
        if segment_mutates(words(seg), predicate):
            return True
    return False


def search_scope_reaches_executor(cmd, cwd):
    """Recursive content search/read whose scope contains the Executor Module without excluding it."""
    rcwd = os.path.realpath(cwd or PROJECT)
    for seg in split_segments(cmd):
        argv = strip_prefix(words(seg))
        if not argv:
            continue
        prog = os.path.basename(argv[0])
        args = argv[1:]
        recursive = (
            prog in RECURSIVE_SEARCH
            or (prog in {"grep", "egrep", "fgrep"} and any(re.match(r"^-[a-zA-Z]*[rR]", a) or a in {"--recursive", "--dereference-recursive"} for a in args))
            or (prog == "git" and args[:1] == ["grep"])
            or (prog == "find" and any(a in {"-exec", "-execdir", "-ok", "-okdir"} for a in args))
            or (prog in {"tar", "zip", "7z"})
            or (prog in {"cp", "rsync", "scp"} and any(re.match(r"^-[a-zA-Z]*[rRa]", a) or a == "--recursive" for a in args))
        )
        if not recursive:
            continue
        if split_exclusions(seg)[1]:
            continue
        operands = []
        skip = False
        for a in args:
            if skip:
                skip = False
                continue
            if a in VALUE_FLAGS:
                skip = True
                continue
            if a.startswith("-") or a.startswith("!") or a.startswith("("):
                if prog == "find":
                    break
                continue
            operands.append(a)
        if prog == "git":
            operands = operands[1:]
        if prog in RECURSIVE_SEARCH | {"grep", "egrep", "fgrep", "git"} and not any(f in args for f in ("-e", "-f", "--regexp", "--file")):
            operands = operands[1:]
        if prog in {"cp", "rsync", "scp"}:
            operands = operands[:-1]
        scopes = [resolve(a, rcwd) for a in operands if "\x00" not in a] or [rcwd]
        if any(within(EXECUTOR, s) or glob_reaches_executor(s) for s in scopes):
            return True
    return False


VALUE_FLAGS = {
    "-g", "--glob", "--iglob", "-t", "--type", "-T", "--type-not", "-e", "--regexp", "-f", "--file",
    "-m", "--max-count", "-A", "-B", "-C", "--context", "--after-context", "--before-context",
    "-d", "--max-depth", "--include", "--exclude", "--exclude-dir", "-name", "-iname", "-path",
    "-ipath", "-type", "-maxdepth", "-mindepth", "-newer", "-size", "-mtime", "-C",
}


def string_values(obj, key_filter=None, key=""):
    if isinstance(obj, str):
        if key_filter is None or key_filter.search(key or ""):
            yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from string_values(v, key_filter, k)
    elif isinstance(obj, list):
        for v in obj:
            yield from string_values(v, key_filter, key)


# ----------------------------------------------------------------------------- events

def on_prompt(data, store):
    session = data.get("session_id")
    if not session:
        raise ValueError("session_id missing")
    prompt = data.get("prompt") or ""
    grants = load_grants(store)
    if re.match(r"^\s*/" + re.escape(NATIVE_IMPLEMENT) + r"(\s|$)", prompt):
        source = data.get("source")
        prompt_id = data.get("prompt_id")
        if data.get("agent_id") or source not in (None, "user") or not prompt_id:
            sys.stderr.write(
                "agent-native-read-grant: /my-interface-native-implement must be submitted directly by the Human "
                f"(source={source!r}, prompt_id present={bool(prompt_id)}); invocation rejected.\n")
            sys.exit(2)
        grants[session] = {"prompt_id": prompt_id}
        save_grants(store, grants)
        return
    if session in grants:
        del grants[session]
        save_grants(store, grants)


def on_pre_tool(data, store):
    tool = data.get("tool_name") or ""
    tin = data.get("tool_input") or {}
    cwd = data.get("cwd") or PROJECT
    session = data.get("session_id")
    prompt_id = data.get("prompt_id")
    agent_id = data.get("agent_id")
    grant = load_grants(store).get(session) if session else None
    granted = bool(not agent_id and prompt_id and grant and grant.get("prompt_id") == prompt_id)
    FIND_CWD[0] = cwd

    # Agent Native Implement is invoked only by the Human, never through a tool.
    if tool == "Skill":
        name = str(tin.get("skill") or tin.get("command") or tin.get("name") or "").lstrip("/")
        if name.split(":")[-1].split()[0:1] == [NATIVE_IMPLEMENT]:
            deny("a non-Human attempt to invoke Agent Native Implement")
        return

    if tool in {"Edit", "Write", "MultiEdit", "NotebookEdit"}:
        raw = tin.get("file_path") or tin.get("notebook_path") or tin.get("path")
        if not raw:
            deny(f"{tool} without a resolvable target path")
        path = resolve(raw, cwd)
        if is_protected(path):
            deny("a direct Interface or Target mutation")
        if path in INTEGRITY_FILES and not granted:
            deny("a change to the enforcement realization outside Agent Native Implement")
        if STATE_NAME in path:
            deny("a change to the read-grant store")
        return

    if tool == "Read":
        raw = tin.get("file_path") or tin.get("path")
        if raw and within(resolve(raw, cwd), EXECUTOR) and not granted:
            deny("an Executor Module read")
        if raw and STATE_NAME in str(raw):
            deny("access to the read-grant store")
        return

    if tool in {"Grep", "Glob"}:
        scope = resolve(tin.get("path") or cwd, cwd)
        texts = [str(v) for v in (tin.get("path"), tin.get("pattern") if tool == "Glob" else None, tin.get("glob")) if v]
        if granted:
            return
        if within(scope, EXECUTOR) or any(mentions_executor(t, scope) for t in texts):
            deny("an Executor Module search")
        if tool == "Grep" and within(EXECUTOR, scope) and (tin.get("output_mode") in {"content", "count"}):
            filt = tin.get("glob")
            typ = (tin.get("type") or "").lower()
            reaches = True
            if filt and not filt.startswith("!"):
                reaches = any(fnmatch.fnmatch(n, filt) or fnmatch.fnmatch("x/" + n, filt) for n in ("executor.md", "rule.yaml", "rule.yml", "SKILL.md"))
            elif typ:
                reaches = typ in {"md", "markdown", "yaml", "yml"}
            if reaches:
                deny("a content search whose scope includes the Executor Module (narrow `path` or `glob` to exclude .interface/executor/)")
        return

    if tool == "Bash":
        cmd = str(tin.get("command") or "")
        if STATE_NAME in cmd:
            deny("access to the read-grant store")
        if NATIVE_IMPLEMENT in cmd and re.search(r"(?:^|[\s;&|(`/])claude(?:\s|$)", cmd):
            deny("a non-Human attempt to invoke Agent Native Implement")
        protected = lambda tok: mentions_protected(tok) or is_protected(resolve(tok, cwd)) if tok else False
        if bash_mutates(cmd, protected):
            deny("a direct Interface or Target mutation")
        if not granted:
            if bash_mutates(cmd, lambda tok: bool(tok) and (mentions_integrity(tok) or resolve(tok, cwd) in INTEGRITY_FILES)):
                deny("a change to the enforcement realization outside Agent Native Implement")
            if mentions_executor(split_exclusions(cmd)[0], cwd):
                deny("an Executor Module read or search")
            if search_scope_reaches_executor(cmd, cwd):
                deny("a recursive search or copy whose scope includes the Executor Module (scope it to exclude .interface/executor/)")
        return

    if tool in NO_PATH_TOOLS:
        return

    # Any other tool (MCP servers, Artifact, IDE, ...): inspect path-like and code-like inputs.
    values = list(string_values(tin, PATHISH_KEY))
    pathlike = [v for v in values if len(v) < 4096 and "\n" not in v and "\x00" not in v]
    if not granted and (any(mentions_executor(v, cwd) for v in values)
                        or any(within(resolve(v, cwd), EXECUTOR) for v in pathlike)):
        deny("an Executor Module access through " + tool)
    if WRITEISH_TOOL.search(tool) and any(mentions_protected(v) for v in values):
        deny("a possible Interface or Target mutation through " + tool)


def main():
    args = sys.argv[1:]
    if not args or args[0] not in {"prompt", "pre"}:
        raise SystemExit(2)
    state_dir = None
    if "--state-dir" in args:
        state_dir = args[args.index("--state-dir") + 1]
    data = json.load(sys.stdin)
    store = state_file(state_dir)
    if args[0] == "prompt":
        on_prompt(data, store)
    else:
        on_pre_tool(data, store)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException as exc:  # fail closed and visible
        sys.stderr.write(f"interface-boundary-guard failed closed: {type(exc).__name__}: {exc}\n")
        sys.exit(2)
