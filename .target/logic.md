# Logic

Defines the services of the Logic Layer. Each service is exposed through the API Layer as a group with the same name.

**Development:**

- Language: Python

```text
Logic
└── Services
    └── MT5
```

<!-------------------------- MT5 -->
### MT5

Every function of the official MetaTrader 5 Python package, so the Target can work with MetaTrader 5.

Owns the Terminals configuration file and selects the Terminal of every call by its `name`, using that Terminal's `path`.
