# API

Defines the groups of the API Layer. Each group exposes the Logic service with the same name.

**Development:**

- Language: Python
- Framework: FastAPI

```text
API
└── Groups
    ├── Entity
    └── MT5
```

<!-------------------------- Entity -->
### Entity

Exposes the Entity Service.

<!-------------------------- MT5 -->
### MT5

Exposes every function of the MT5 Service, so external programs can work with MetaTrader 5 through the REST API.
