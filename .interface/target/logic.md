# Logic

Defines the services of the Logic Layer. Each service is exposed through the API Layer as a group with the same name.

**Development:**

- Language: Python

```text
Logic
└── Services
    ├── Entity
    └── MT5
```

<!-------------------------- Entity -->
### Entity

Data Entry for every defined Entity. Its operations are defined by the Database Component in Implementation.

<!-------------------------- MT5 -->
### MT5

Every function of the official MetaTrader 5 Python package, so the Target can work with MetaTrader 5.
