# Entities

Defines the project's entities.

**Persistence:** Every Entity declared in this section is persistent. It has an independently stored record and identity that is kept durably. An Entity is non-persistent only when its own definition explicitly declares otherwise.

**Development:**

- Language: Python

```text
Entities
├── User
├── Instance
├── Currency
├── Broker
├── Asset
├── Account Group
└── Account
```

<!-------------------------- User -->
### User

**Purpose:** Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The user's display name.
- `username` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The username used to identify the user.
- `password` — Type: `string`; Nullable: `false`; Purpose: The password credential used by the user.
- `api_key` — Type: `string`; Nullable: `false`; Purpose: The API key assigned to the user.
- `is_active` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the user is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the user.

**Rules:**

- `password` is a credential and must use `hash` storage at rest.
- `api_key` is a credential and must use `hash` storage at rest.

**Initial Data:**

- `name`: `Admin`; `username`: `admin`; `password`: Generate securely; `api_key`: Generate securely.

<!-------------------------- Instance -->
### Instance

**Purpose:** Defines a user-owned connection instance through which the system accesses MetaTrader 5.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `user_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the user who owns this instance.
- `name` — Type: `string`; Nullable: `false`; Purpose: The instance's display name.
- `ip` — Type: `string`; Nullable: `true`; Purpose: Identifies the technical network address used to reach MetaTrader 5 when required.
- `username` — Type: `string`; Nullable: `true`; Purpose: Defines the technical username used to establish the Instance connection when required.
- `password` — Type: `string`; Nullable: `true`; Purpose: Defines the technical password used to establish the Instance connection when required.
- `api_key` — Type: `string`; Nullable: `true`; Purpose: Defines the technical API credential used to establish the Instance connection when required.
- `is_active` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the instance is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the instance.

**Relationships:**

- Belongs to one User through `user_id`.

**Rules:**

- `password` and `api_key` are credentials and must use `encrypted` storage at rest.
- MetaTrader 5 defines which connection fields are required; every field it requires must be present before the Instance can be used.
- The combination of `user_id` and `name` must be unique.

**Initial Data:**

- `name`: `MetaTrader`; `user_id`: `1`; `ip`: `127.0.0.1`; `username`: `test`; `password`: Generate securely; `api_key`: Generate securely.

<!-------------------------- Currency -->
### Currency

**Purpose:** Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `user_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the user who owns this currency.
- `code` — Type: `string`; Size: `3`; Nullable: `false`; Purpose: The currency's standard three-letter code, such as `USD` or `EUR`.
- `symbol` — Type: `string`; Nullable: `true`; Purpose: The currency's display symbol, such as `$`, `€`, or `£`.
- `country` — Type: `string`; Nullable: `true`; Purpose: Identifies the country or region associated with the currency.
- `decimal_digits` — Type: `integer`; Nullable: `false`; Default: `2`; Purpose: Defines the number of decimal digits normally used for monetary values in the currency.
- `is_active` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the currency is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the currency.

**Relationships:**

- Belongs to one User through `user_id`.

**Rules:**

- The combination of `user_id` and `code` must be unique.

**Initial Data:**

- `user_id`: `1`; `code`: `USD`; `symbol`: `$`; `country`: `United States`; `decimal_digits`: `2`.
- `user_id`: `1`; `code`: `EUR`; `symbol`: `€`; `country`: `Eurozone`; `decimal_digits`: `2`.
- `user_id`: `1`; `code`: `GBP`; `symbol`: `£`; `country`: `United Kingdom`; `decimal_digits`: `2`.
- `user_id`: `1`; `code`: `JPY`; `symbol`: `¥`; `country`: `Japan`; `decimal_digits`: `0`.
- `user_id`: `1`; `code`: `CHF`; `symbol`: `CHF`; `country`: `Switzerland`; `decimal_digits`: `2`.
- `user_id`: `1`; `code`: `CAD`; `symbol`: `C$`; `country`: `Canada`; `decimal_digits`: `2`.
- `user_id`: `1`; `code`: `AUD`; `symbol`: `A$`; `country`: `Australia`; `decimal_digits`: `2`.
- `user_id`: `1`; `code`: `NZD`; `symbol`: `NZ$`; `country`: `New Zealand`; `decimal_digits`: `2`.

<!-------------------------- Broker -->
### Broker

**Purpose:** Defines a broker supported by the system and identifies the user who owns its configuration.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Purpose: The broker's display name.
- `user_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the user who owns the broker configuration.
- `is_active` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the broker is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the broker.

**Relationships:**

- Belongs to one User through `user_id`.

**Rules:**

- The combination of `user_id` and `name` must be unique.

**Initial Data:**

- `name`: `FxPro`; `user_id`: `1`.

<!-------------------------- Asset -->
### Asset

**Purpose:** Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `broker_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the broker that provides this asset.
- `symbol` — Type: `string`; Nullable: `false`; Purpose: Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.
- `category` — Type: `string`; Nullable: `false`; Purpose: Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.
- `point_size` — Type: `float`; Nullable: `false`; Default: `0.0`; Purpose: Stores the size of one point for the asset.
- `digits` — Type: `integer`; Nullable: `false`; Default: `0`; Purpose: Stores the number of decimal digits used for the asset's price.
- `is_active` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the asset is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the asset.

**Relationships:**

- Belongs to one Broker through `broker_id`.

**Rules:**

- The combination of `broker_id` and `symbol` must be unique.

**Initial Data:**

- `broker_id`: `1`; `symbol`: `EUR/USD`; `category`: `Currency`; `point_size`: `0.0001`; `digits`: `5`.
- `broker_id`: `1`; `symbol`: `EUR/GBP`; `category`: `Currency`; `point_size`: `0.001`; `digits`: `5`.
- `broker_id`: `1`; `symbol`: `XAU/USD`; `category`: `Commodity`; `point_size`: `0.01`; `digits`: `2`.
- `broker_id`: `1`; `symbol`: `USOil`; `category`: `Commodity`; `point_size`: `0.01`; `digits`: `3`.

<!-------------------------- Account Group -->
### Account Group

**Purpose:** Defines an independent group for organizing trading accounts owned by one user.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `user_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the user who owns the account group.
- `name` — Type: `string`; Nullable: `false`; Purpose: The account group's display name.
- `is_active` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the account group is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the account group.

**Relationships:**

- Belongs to one User through `user_id`.

**Rules:**

- The combination of `user_id` and `name` must be unique.

**Initial Data:**

- `user_id`: `1`; `name`: `Default`.

<!-------------------------- Account -->
### Account

**Purpose:** Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to MetaTrader 5.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The account's display name.
- `group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the account group that contains the account.
- `broker_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the broker that owns the account.
- `instance_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the trading-platform instance used to connect this account.
- `base_currency_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the base currency used by the account.
- `username` — Type: `string`; Nullable: `false`; Purpose: The username identifier used to access the trading account.
- `password` — Type: `string`; Nullable: `false`; Purpose: The credential used to access the trading account.
- `leverage` — Type: `integer`; Nullable: `false`; Purpose: Defines the account's leverage multiplier.
- `balance` — Type: `decimal`; Nullable: `false`; Default: `0`; Purpose: Stores the account's current balance.
- `account_type` — Type: `string`; Nullable: `false`; Purpose: Identifies the account model, such as `cfd` or `spread_betting`.
- `is_active` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the account is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the account.

**Relationships:**

- Belongs to one Account Group through `group_id`.
- Belongs to one Broker through `broker_id`.
- Uses one Instance through `instance_id`.
- Uses one Currency as its base currency through `base_currency_id`.

**Rules:**

- `password` is a credential and must use `encrypted` storage at rest.
- Instance credentials authenticate the technical MetaTrader 5 connection; Account credentials authenticate this specific trading account. The same credential must not be duplicated across both Entities unless MetaTrader 5 explicitly requires it in both roles.
- The combination of `group_id`, `broker_id`, and `instance_id` must be unique.

**Initial Data:**

- `name`: `Acc-1`; `group_id`: `1`; `broker_id`: `1`; `instance_id`: `1`; `base_currency_id`: `1`; `username`: `test`; `password`: Generate securely; `leverage`: `100`; `account_type`: `CFD`.
