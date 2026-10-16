/** The metadata of every Entity, generated from the Entity Declarations. */

export type FieldType =
  | "string"
  | "integer"
  | "float"
  | "decimal"
  | "boolean"
  | "datetime"
  | "date"
  | "time"
  | "uuid";

export interface FieldMeta {
  readonly name: string;
  readonly type: FieldType;
  readonly description: string | null;
  readonly nullable: boolean;
  readonly required: boolean;
  readonly sensitive: boolean;
  readonly immutable: boolean;
  readonly generated: boolean;
  readonly size: number | null;
  readonly relation: { readonly resource: string; readonly field: string } | null;
}

export interface EntityMeta {
  readonly name: string;
  readonly resource: string;
  readonly route: string;
  readonly label: string;
  readonly description: string | null;
  readonly fields: readonly FieldMeta[];
  readonly dependsOn: Readonly<Record<string, string>>;
}

export const entities: readonly EntityMeta[] = [
  {
    "name": "User",
    "resource": "user",
    "route": "/user",
    "label": "name",
    "description": "Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.",
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "description": null,
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": true,
        "generated": true,
        "size": null,
        "relation": null
      },
      {
        "name": "name",
        "type": "string",
        "description": "The user's display name.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "username",
        "type": "string",
        "description": "The username used to identify the user.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "password",
        "type": "string",
        "description": "The password credential used by the user.",
        "nullable": false,
        "required": true,
        "sensitive": true,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "api_key",
        "type": "string",
        "description": "The API key assigned to the user.",
        "nullable": false,
        "required": true,
        "sensitive": true,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "is_active",
        "type": "boolean",
        "description": "Indicates whether the user is active.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "description",
        "type": "string",
        "description": "Describes the user.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      }
    ],
    "dependsOn": {}
  },
  {
    "name": "Instance",
    "resource": "instance",
    "route": "/instance",
    "label": "name",
    "description": "Defines a user-owned connection instance through which the system accesses MetaTrader 5.",
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "description": null,
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": true,
        "generated": true,
        "size": null,
        "relation": null
      },
      {
        "name": "user_id",
        "type": "integer",
        "description": "Identifies the user who owns this instance.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "user",
          "field": "id"
        }
      },
      {
        "name": "name",
        "type": "string",
        "description": "The instance's display name.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "ip",
        "type": "string",
        "description": "Identifies the technical network address used to reach MetaTrader 5 when required.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "path",
        "type": "string",
        "description": "The local filesystem path of the MetaTrader 5 terminal executable used by this Instance when required.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "username",
        "type": "string",
        "description": "Defines the technical username used to establish the Instance connection when required.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "password",
        "type": "string",
        "description": "Defines the technical password used to establish the Instance connection when required.",
        "nullable": true,
        "required": false,
        "sensitive": true,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "api_key",
        "type": "string",
        "description": "Defines the technical API credential used to establish the Instance connection when required.",
        "nullable": true,
        "required": false,
        "sensitive": true,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "is_active",
        "type": "boolean",
        "description": "Indicates whether the instance is active.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "description",
        "type": "string",
        "description": "Describes the instance.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      }
    ],
    "dependsOn": {}
  },
  {
    "name": "Currency",
    "resource": "currency",
    "route": "/currency",
    "label": "code",
    "description": "Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "description": null,
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": true,
        "generated": true,
        "size": null,
        "relation": null
      },
      {
        "name": "user_id",
        "type": "integer",
        "description": "Identifies the user who owns this currency.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "user",
          "field": "id"
        }
      },
      {
        "name": "code",
        "type": "string",
        "description": "The currency's standard three-letter code, such as `USD` or `EUR`.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": 3,
        "relation": null
      },
      {
        "name": "symbol",
        "type": "string",
        "description": "The currency's display symbol, such as `$`, `€`, or `£`.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "country",
        "type": "string",
        "description": "Identifies the country or region associated with the currency.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "decimal_digits",
        "type": "integer",
        "description": "Defines the number of decimal digits normally used for monetary values in the currency.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "is_active",
        "type": "boolean",
        "description": "Indicates whether the currency is active.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "description",
        "type": "string",
        "description": "Describes the currency.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      }
    ],
    "dependsOn": {}
  },
  {
    "name": "Broker",
    "resource": "broker",
    "route": "/broker",
    "label": "name",
    "description": "Defines a broker supported by the system and identifies the user who owns its configuration.",
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "description": null,
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": true,
        "generated": true,
        "size": null,
        "relation": null
      },
      {
        "name": "name",
        "type": "string",
        "description": "The broker's display name.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "user_id",
        "type": "integer",
        "description": "Identifies the user who owns the broker configuration.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "user",
          "field": "id"
        }
      },
      {
        "name": "is_active",
        "type": "boolean",
        "description": "Indicates whether the broker is active.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "description",
        "type": "string",
        "description": "Describes the broker.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      }
    ],
    "dependsOn": {}
  },
  {
    "name": "Asset",
    "resource": "asset",
    "route": "/asset",
    "label": "symbol",
    "description": "Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "description": null,
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": true,
        "generated": true,
        "size": null,
        "relation": null
      },
      {
        "name": "broker_id",
        "type": "integer",
        "description": "Identifies the broker that provides this asset.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "broker",
          "field": "id"
        }
      },
      {
        "name": "symbol",
        "type": "string",
        "description": "Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "category",
        "type": "string",
        "description": "Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "point_size",
        "type": "float",
        "description": "Stores the size of one point for the asset.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "digits",
        "type": "integer",
        "description": "Stores the number of decimal digits used for the asset's price.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "is_active",
        "type": "boolean",
        "description": "Indicates whether the asset is active.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "description",
        "type": "string",
        "description": "Describes the asset.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      }
    ],
    "dependsOn": {}
  },
  {
    "name": "Account Group",
    "resource": "account_group",
    "route": "/account_group",
    "label": "name",
    "description": "Defines an independent group for organizing trading accounts owned by one user.",
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "description": null,
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": true,
        "generated": true,
        "size": null,
        "relation": null
      },
      {
        "name": "user_id",
        "type": "integer",
        "description": "Identifies the user who owns the account group.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "user",
          "field": "id"
        }
      },
      {
        "name": "name",
        "type": "string",
        "description": "The account group's display name.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "is_active",
        "type": "boolean",
        "description": "Indicates whether the account group is active.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "description",
        "type": "string",
        "description": "Describes the account group.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      }
    ],
    "dependsOn": {}
  },
  {
    "name": "Account",
    "resource": "account",
    "route": "/account",
    "label": "name",
    "description": "Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to MetaTrader 5.",
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "description": null,
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": true,
        "generated": true,
        "size": null,
        "relation": null
      },
      {
        "name": "name",
        "type": "string",
        "description": "The account's display name.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "group_id",
        "type": "integer",
        "description": "Identifies the account group that contains the account.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "account_group",
          "field": "id"
        }
      },
      {
        "name": "broker_id",
        "type": "integer",
        "description": "Identifies the broker that owns the account.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "broker",
          "field": "id"
        }
      },
      {
        "name": "instance_id",
        "type": "integer",
        "description": "Identifies the trading-platform instance used to connect this account.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "instance",
          "field": "id"
        }
      },
      {
        "name": "base_currency_id",
        "type": "integer",
        "description": "Identifies the base currency used by the account.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": {
          "resource": "currency",
          "field": "id"
        }
      },
      {
        "name": "username",
        "type": "string",
        "description": "The username identifier used to access the trading account.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "password",
        "type": "string",
        "description": "The credential used to access the trading account.",
        "nullable": false,
        "required": true,
        "sensitive": true,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "leverage",
        "type": "integer",
        "description": "Defines the account's leverage multiplier.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "balance",
        "type": "decimal",
        "description": "Stores the account's current balance.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "account_type",
        "type": "string",
        "description": "Identifies the account model, such as `cfd` or `spread_betting`.",
        "nullable": false,
        "required": true,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "is_active",
        "type": "boolean",
        "description": "Indicates whether the account is active.",
        "nullable": false,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      },
      {
        "name": "description",
        "type": "string",
        "description": "Describes the account.",
        "nullable": true,
        "required": false,
        "sensitive": false,
        "immutable": false,
        "generated": false,
        "size": null,
        "relation": null
      }
    ],
    "dependsOn": {}
  }
];

/** The metadata of one Entity by its resource. */
export function entityOf(resource: string): EntityMeta {
  const found = entities.find((item) => item.resource === resource);
  if (found === undefined) {
    throw new Error(`Unknown resource ${resource}`);
  }
  return found;
}
