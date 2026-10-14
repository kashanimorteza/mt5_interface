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

Implements every function of the official MetaTrader 5 Python package (MetaTrader5), so the Target can work with MetaTrader 5 through this service.

- The functions are organized in the same groups as the package; each group is a separate class that can be imported on its own.
- The exact functions and groups are taken from the package's official documentation when the service is implemented.
