# API

Defines the groups of the API Layer. Each group exposes the Logic service with the same name.

**Development:**

- Language: Python
- Framework: FastAPI

```text
API
└── Groups
    └── MT5
```

<!-------------------------- MT5 -->
### MT5

Exposes every function of the MT5 Service, so external programs can work with MetaTrader 5 through the REST API.

Every request names its Terminal by `name`.
