# Logic

Defines the services of the Logic Layer. The MT5 Service is exposed through the API Layer as a group with the same name; the MT5 Client Service calls that group and is not exposed.

**Development:**

- Language: Python

```text
Logic
└── Services
    ├── MT5
    └── MT5 Client
```

<!-------------------------- MT5 -->
### MT5

Every function of the official MetaTrader 5 Python package, so the Target can work with MetaTrader 5.

<!-------------------------- MT5 Client -->
### MT5 Client

Every function of the MT5 Service, run on a remote MT5 Interface API through its Endpoints, in the same shape as the MT5 Service, so a program can work with MetaTrader 5 from any operating system.
