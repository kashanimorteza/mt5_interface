export interface paths {
    "/entity/user/add": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Add
         * @description Store one complete new Entity and return it as stored, with generated values.
         */
        post: operations["add_entity_user_add_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/update": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * Update
         * @description Replace every mutable Field of the record the Entity's id locates, or return None.
         */
        put: operations["update_entity_user_update_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/list": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * List
         * @description Return the matching Entities, ordered and bounded by a positive limit.
         */
        post: operations["list_entity_user_list_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/get_by_id/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get By Id
         * @description Return the Entity with this id, or None.
         */
        get: operations["get_by_id_entity_user_get_by_id__id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/delete/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Delete
         * @description Delete the Entity with this id and return it as it was, or None.
         */
        delete: operations["delete_entity_user_delete__id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/enable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Enable
         * @description Set only is_active to true and return the final Entity, or None.
         */
        patch: operations["enable_entity_user_enable__id__patch"];
        trace?: never;
    };
    "/entity/user/disable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Disable
         * @description Set only is_active to false and return the final Entity, or None.
         */
        patch: operations["disable_entity_user_disable__id__patch"];
        trace?: never;
    };
    "/entity/user/count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Count
         * @description Return the number of matching records.
         */
        post: operations["count_entity_user_count_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/sum": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Sum
         * @description Return the total of one numeric Field over matching records, or zero.
         */
        post: operations["sum_entity_user_sum_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/min": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Min
         * @description Return the smallest value of one Field over matching records, or None.
         */
        post: operations["min_entity_user_min_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/max": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Max
         * @description Return the largest value of one Field over matching records, or None.
         */
        post: operations["max_entity_user_max_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/user/truncate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Truncate
         * @description Delete every record of the Entity, keeping its Table, and return the count.
         */
        delete: operations["truncate_entity_user_truncate_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/add": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Add
         * @description Store one complete new Entity and return it as stored, with generated values.
         */
        post: operations["add_entity_instance_add_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/update": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * Update
         * @description Replace every mutable Field of the record the Entity's id locates, or return None.
         */
        put: operations["update_entity_instance_update_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/list": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * List
         * @description Return the matching Entities, ordered and bounded by a positive limit.
         */
        post: operations["list_entity_instance_list_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/get_by_id/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get By Id
         * @description Return the Entity with this id, or None.
         */
        get: operations["get_by_id_entity_instance_get_by_id__id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/delete/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Delete
         * @description Delete the Entity with this id and return it as it was, or None.
         */
        delete: operations["delete_entity_instance_delete__id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/enable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Enable
         * @description Set only is_active to true and return the final Entity, or None.
         */
        patch: operations["enable_entity_instance_enable__id__patch"];
        trace?: never;
    };
    "/entity/instance/disable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Disable
         * @description Set only is_active to false and return the final Entity, or None.
         */
        patch: operations["disable_entity_instance_disable__id__patch"];
        trace?: never;
    };
    "/entity/instance/count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Count
         * @description Return the number of matching records.
         */
        post: operations["count_entity_instance_count_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/sum": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Sum
         * @description Return the total of one numeric Field over matching records, or zero.
         */
        post: operations["sum_entity_instance_sum_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/min": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Min
         * @description Return the smallest value of one Field over matching records, or None.
         */
        post: operations["min_entity_instance_min_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/max": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Max
         * @description Return the largest value of one Field over matching records, or None.
         */
        post: operations["max_entity_instance_max_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/instance/truncate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Truncate
         * @description Delete every record of the Entity, keeping its Table, and return the count.
         */
        delete: operations["truncate_entity_instance_truncate_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/add": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Add
         * @description Store one complete new Entity and return it as stored, with generated values.
         */
        post: operations["add_entity_currency_add_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/update": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * Update
         * @description Replace every mutable Field of the record the Entity's id locates, or return None.
         */
        put: operations["update_entity_currency_update_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/list": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * List
         * @description Return the matching Entities, ordered and bounded by a positive limit.
         */
        post: operations["list_entity_currency_list_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/get_by_id/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get By Id
         * @description Return the Entity with this id, or None.
         */
        get: operations["get_by_id_entity_currency_get_by_id__id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/delete/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Delete
         * @description Delete the Entity with this id and return it as it was, or None.
         */
        delete: operations["delete_entity_currency_delete__id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/enable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Enable
         * @description Set only is_active to true and return the final Entity, or None.
         */
        patch: operations["enable_entity_currency_enable__id__patch"];
        trace?: never;
    };
    "/entity/currency/disable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Disable
         * @description Set only is_active to false and return the final Entity, or None.
         */
        patch: operations["disable_entity_currency_disable__id__patch"];
        trace?: never;
    };
    "/entity/currency/count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Count
         * @description Return the number of matching records.
         */
        post: operations["count_entity_currency_count_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/sum": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Sum
         * @description Return the total of one numeric Field over matching records, or zero.
         */
        post: operations["sum_entity_currency_sum_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/min": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Min
         * @description Return the smallest value of one Field over matching records, or None.
         */
        post: operations["min_entity_currency_min_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/max": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Max
         * @description Return the largest value of one Field over matching records, or None.
         */
        post: operations["max_entity_currency_max_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/currency/truncate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Truncate
         * @description Delete every record of the Entity, keeping its Table, and return the count.
         */
        delete: operations["truncate_entity_currency_truncate_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/add": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Add
         * @description Store one complete new Entity and return it as stored, with generated values.
         */
        post: operations["add_entity_broker_add_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/update": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * Update
         * @description Replace every mutable Field of the record the Entity's id locates, or return None.
         */
        put: operations["update_entity_broker_update_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/list": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * List
         * @description Return the matching Entities, ordered and bounded by a positive limit.
         */
        post: operations["list_entity_broker_list_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/get_by_id/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get By Id
         * @description Return the Entity with this id, or None.
         */
        get: operations["get_by_id_entity_broker_get_by_id__id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/delete/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Delete
         * @description Delete the Entity with this id and return it as it was, or None.
         */
        delete: operations["delete_entity_broker_delete__id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/enable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Enable
         * @description Set only is_active to true and return the final Entity, or None.
         */
        patch: operations["enable_entity_broker_enable__id__patch"];
        trace?: never;
    };
    "/entity/broker/disable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Disable
         * @description Set only is_active to false and return the final Entity, or None.
         */
        patch: operations["disable_entity_broker_disable__id__patch"];
        trace?: never;
    };
    "/entity/broker/count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Count
         * @description Return the number of matching records.
         */
        post: operations["count_entity_broker_count_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/sum": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Sum
         * @description Return the total of one numeric Field over matching records, or zero.
         */
        post: operations["sum_entity_broker_sum_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/min": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Min
         * @description Return the smallest value of one Field over matching records, or None.
         */
        post: operations["min_entity_broker_min_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/max": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Max
         * @description Return the largest value of one Field over matching records, or None.
         */
        post: operations["max_entity_broker_max_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/broker/truncate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Truncate
         * @description Delete every record of the Entity, keeping its Table, and return the count.
         */
        delete: operations["truncate_entity_broker_truncate_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/add": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Add
         * @description Store one complete new Entity and return it as stored, with generated values.
         */
        post: operations["add_entity_asset_add_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/update": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * Update
         * @description Replace every mutable Field of the record the Entity's id locates, or return None.
         */
        put: operations["update_entity_asset_update_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/list": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * List
         * @description Return the matching Entities, ordered and bounded by a positive limit.
         */
        post: operations["list_entity_asset_list_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/get_by_id/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get By Id
         * @description Return the Entity with this id, or None.
         */
        get: operations["get_by_id_entity_asset_get_by_id__id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/delete/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Delete
         * @description Delete the Entity with this id and return it as it was, or None.
         */
        delete: operations["delete_entity_asset_delete__id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/enable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Enable
         * @description Set only is_active to true and return the final Entity, or None.
         */
        patch: operations["enable_entity_asset_enable__id__patch"];
        trace?: never;
    };
    "/entity/asset/disable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Disable
         * @description Set only is_active to false and return the final Entity, or None.
         */
        patch: operations["disable_entity_asset_disable__id__patch"];
        trace?: never;
    };
    "/entity/asset/count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Count
         * @description Return the number of matching records.
         */
        post: operations["count_entity_asset_count_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/sum": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Sum
         * @description Return the total of one numeric Field over matching records, or zero.
         */
        post: operations["sum_entity_asset_sum_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/min": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Min
         * @description Return the smallest value of one Field over matching records, or None.
         */
        post: operations["min_entity_asset_min_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/max": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Max
         * @description Return the largest value of one Field over matching records, or None.
         */
        post: operations["max_entity_asset_max_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/asset/truncate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Truncate
         * @description Delete every record of the Entity, keeping its Table, and return the count.
         */
        delete: operations["truncate_entity_asset_truncate_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/add": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Add
         * @description Store one complete new Entity and return it as stored, with generated values.
         */
        post: operations["add_entity_account_group_add_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/update": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * Update
         * @description Replace every mutable Field of the record the Entity's id locates, or return None.
         */
        put: operations["update_entity_account_group_update_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/list": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * List
         * @description Return the matching Entities, ordered and bounded by a positive limit.
         */
        post: operations["list_entity_account_group_list_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/get_by_id/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get By Id
         * @description Return the Entity with this id, or None.
         */
        get: operations["get_by_id_entity_account_group_get_by_id__id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/delete/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Delete
         * @description Delete the Entity with this id and return it as it was, or None.
         */
        delete: operations["delete_entity_account_group_delete__id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/enable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Enable
         * @description Set only is_active to true and return the final Entity, or None.
         */
        patch: operations["enable_entity_account_group_enable__id__patch"];
        trace?: never;
    };
    "/entity/account_group/disable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Disable
         * @description Set only is_active to false and return the final Entity, or None.
         */
        patch: operations["disable_entity_account_group_disable__id__patch"];
        trace?: never;
    };
    "/entity/account_group/count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Count
         * @description Return the number of matching records.
         */
        post: operations["count_entity_account_group_count_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/sum": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Sum
         * @description Return the total of one numeric Field over matching records, or zero.
         */
        post: operations["sum_entity_account_group_sum_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/min": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Min
         * @description Return the smallest value of one Field over matching records, or None.
         */
        post: operations["min_entity_account_group_min_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/max": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Max
         * @description Return the largest value of one Field over matching records, or None.
         */
        post: operations["max_entity_account_group_max_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account_group/truncate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Truncate
         * @description Delete every record of the Entity, keeping its Table, and return the count.
         */
        delete: operations["truncate_entity_account_group_truncate_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/add": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Add
         * @description Store one complete new Entity and return it as stored, with generated values.
         */
        post: operations["add_entity_account_add_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/update": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        /**
         * Update
         * @description Replace every mutable Field of the record the Entity's id locates, or return None.
         */
        put: operations["update_entity_account_update_put"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/list": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * List
         * @description Return the matching Entities, ordered and bounded by a positive limit.
         */
        post: operations["list_entity_account_list_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/get_by_id/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get By Id
         * @description Return the Entity with this id, or None.
         */
        get: operations["get_by_id_entity_account_get_by_id__id__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/delete/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Delete
         * @description Delete the Entity with this id and return it as it was, or None.
         */
        delete: operations["delete_entity_account_delete__id__delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/enable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Enable
         * @description Set only is_active to true and return the final Entity, or None.
         */
        patch: operations["enable_entity_account_enable__id__patch"];
        trace?: never;
    };
    "/entity/account/disable/{id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Disable
         * @description Set only is_active to false and return the final Entity, or None.
         */
        patch: operations["disable_entity_account_disable__id__patch"];
        trace?: never;
    };
    "/entity/account/count": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Count
         * @description Return the number of matching records.
         */
        post: operations["count_entity_account_count_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/sum": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Sum
         * @description Return the total of one numeric Field over matching records, or zero.
         */
        post: operations["sum_entity_account_sum_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/min": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Min
         * @description Return the smallest value of one Field over matching records, or None.
         */
        post: operations["min_entity_account_min_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/max": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /**
         * Max
         * @description Return the largest value of one Field over matching records, or None.
         */
        post: operations["max_entity_account_max_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/entity/account/truncate": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        post?: never;
        /**
         * Truncate
         * @description Delete every record of the Entity, keeping its Table, and return the count.
         */
        delete: operations["truncate_entity_account_truncate_delete"];
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** Body_add_entity_account_add_post */
        Body_add_entity_account_add_post: {
            /** Account */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_add_entity_account_group_add_post */
        Body_add_entity_account_group_add_post: {
            /** AccountGroup */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_add_entity_asset_add_post */
        Body_add_entity_asset_add_post: {
            /** Asset */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_add_entity_broker_add_post */
        Body_add_entity_broker_add_post: {
            /** Broker */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_add_entity_currency_add_post */
        Body_add_entity_currency_add_post: {
            /** Currency */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_add_entity_instance_add_post */
        Body_add_entity_instance_add_post: {
            /** Instance */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_add_entity_user_add_post */
        Body_add_entity_user_add_post: {
            /** User */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_count_entity_account_count_post */
        Body_count_entity_account_count_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_count_entity_account_group_count_post */
        Body_count_entity_account_group_count_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_count_entity_asset_count_post */
        Body_count_entity_asset_count_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_count_entity_broker_count_post */
        Body_count_entity_broker_count_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_count_entity_currency_count_post */
        Body_count_entity_currency_count_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_count_entity_instance_count_post */
        Body_count_entity_instance_count_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_count_entity_user_count_post */
        Body_count_entity_user_count_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_disable_entity_account_disable__id__patch */
        Body_disable_entity_account_disable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_disable_entity_account_group_disable__id__patch */
        Body_disable_entity_account_group_disable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_disable_entity_asset_disable__id__patch */
        Body_disable_entity_asset_disable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_disable_entity_broker_disable__id__patch */
        Body_disable_entity_broker_disable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_disable_entity_currency_disable__id__patch */
        Body_disable_entity_currency_disable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_disable_entity_instance_disable__id__patch */
        Body_disable_entity_instance_disable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_disable_entity_user_disable__id__patch */
        Body_disable_entity_user_disable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_enable_entity_account_enable__id__patch */
        Body_enable_entity_account_enable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_enable_entity_account_group_enable__id__patch */
        Body_enable_entity_account_group_enable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_enable_entity_asset_enable__id__patch */
        Body_enable_entity_asset_enable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_enable_entity_broker_enable__id__patch */
        Body_enable_entity_broker_enable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_enable_entity_currency_enable__id__patch */
        Body_enable_entity_currency_enable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_enable_entity_instance_enable__id__patch */
        Body_enable_entity_instance_enable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_enable_entity_user_enable__id__patch */
        Body_enable_entity_user_enable__id__patch: {
            /** Instance */
            instance?: string | null;
        };
        /** Body_list_entity_account_group_list_post */
        Body_list_entity_account_group_list_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Orders */
            orders?: components["schemas"]["OrderForm"][] | null;
            /** Limit */
            limit?: number | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_list_entity_account_list_post */
        Body_list_entity_account_list_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Orders */
            orders?: components["schemas"]["OrderForm"][] | null;
            /** Limit */
            limit?: number | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_list_entity_asset_list_post */
        Body_list_entity_asset_list_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Orders */
            orders?: components["schemas"]["OrderForm"][] | null;
            /** Limit */
            limit?: number | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_list_entity_broker_list_post */
        Body_list_entity_broker_list_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Orders */
            orders?: components["schemas"]["OrderForm"][] | null;
            /** Limit */
            limit?: number | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_list_entity_currency_list_post */
        Body_list_entity_currency_list_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Orders */
            orders?: components["schemas"]["OrderForm"][] | null;
            /** Limit */
            limit?: number | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_list_entity_instance_list_post */
        Body_list_entity_instance_list_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Orders */
            orders?: components["schemas"]["OrderForm"][] | null;
            /** Limit */
            limit?: number | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_list_entity_user_list_post */
        Body_list_entity_user_list_post: {
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Orders */
            orders?: components["schemas"]["OrderForm"][] | null;
            /** Limit */
            limit?: number | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_max_entity_account_group_max_post */
        Body_max_entity_account_group_max_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_max_entity_account_max_post */
        Body_max_entity_account_max_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_max_entity_asset_max_post */
        Body_max_entity_asset_max_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_max_entity_broker_max_post */
        Body_max_entity_broker_max_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_max_entity_currency_max_post */
        Body_max_entity_currency_max_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_max_entity_instance_max_post */
        Body_max_entity_instance_max_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_max_entity_user_max_post */
        Body_max_entity_user_max_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_min_entity_account_group_min_post */
        Body_min_entity_account_group_min_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_min_entity_account_min_post */
        Body_min_entity_account_min_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_min_entity_asset_min_post */
        Body_min_entity_asset_min_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_min_entity_broker_min_post */
        Body_min_entity_broker_min_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_min_entity_currency_min_post */
        Body_min_entity_currency_min_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_min_entity_instance_min_post */
        Body_min_entity_instance_min_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_min_entity_user_min_post */
        Body_min_entity_user_min_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_sum_entity_account_group_sum_post */
        Body_sum_entity_account_group_sum_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_sum_entity_account_sum_post */
        Body_sum_entity_account_sum_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_sum_entity_asset_sum_post */
        Body_sum_entity_asset_sum_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_sum_entity_broker_sum_post */
        Body_sum_entity_broker_sum_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_sum_entity_currency_sum_post */
        Body_sum_entity_currency_sum_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_sum_entity_instance_sum_post */
        Body_sum_entity_instance_sum_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_sum_entity_user_sum_post */
        Body_sum_entity_user_sum_post: {
            /** Field */
            field: string;
            /** Filters */
            filters?: components["schemas"]["FilterForm"][] | null;
            combination?: components["schemas"]["FilterCombination"] | null;
            /** Instance */
            instance?: string | null;
        };
        /** Body_update_entity_account_group_update_put */
        Body_update_entity_account_group_update_put: {
            /** AccountGroup */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_update_entity_account_update_put */
        Body_update_entity_account_update_put: {
            /** Account */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_update_entity_asset_update_put */
        Body_update_entity_asset_update_put: {
            /** Asset */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_update_entity_broker_update_put */
        Body_update_entity_broker_update_put: {
            /** Broker */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_update_entity_currency_update_put */
        Body_update_entity_currency_update_put: {
            /** Currency */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_update_entity_instance_update_put */
        Body_update_entity_instance_update_put: {
            /** Instance */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /** Body_update_entity_user_update_put */
        Body_update_entity_user_update_put: {
            /** User */
            entity: {
                [key: string]: unknown;
            };
            /** Instance */
            instance?: string | null;
        };
        /**
         * FilterCombination
         * @description How several Filters combine.
         * @enum {string}
         */
        FilterCombination: "AND" | "OR";
        /**
         * FilterForm
         * @description A Filter as it travels: its Field's name, its operator, and its value.
         */
        FilterForm: {
            /** Field */
            field: string;
            operator: components["schemas"]["FilterOperator"];
            /** Value */
            value?: unknown;
        };
        /**
         * FilterOperator
         * @description How a Filter compares a Field with its value.
         * @enum {string}
         */
        FilterOperator: "EQUALS" | "NOT_EQUALS" | "GREATER_THAN" | "GREATER_OR_EQUAL" | "LESS_THAN" | "LESS_OR_EQUAL" | "IN" | "CONTAINS" | "STARTS_WITH" | "ENDS_WITH" | "IS_NULL" | "IS_NOT_NULL";
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /**
         * OrderDirection
         * @description The direction of an Order.
         * @enum {string}
         */
        OrderDirection: "ASCENDING" | "DESCENDING";
        /**
         * OrderForm
         * @description An Order as it travels: its Field's name and its direction.
         */
        OrderForm: {
            /** Field */
            field: string;
            /** @default ASCENDING */
            direction: components["schemas"]["OrderDirection"];
        };
        /** ValidationError */
        ValidationError: {
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
            /** Input */
            input?: unknown;
            /** Context */
            ctx?: Record<string, never>;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    add_entity_user_add_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_add_entity_user_add_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_entity_user_update_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_update_entity_user_update_put"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_entity_user_list_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_list_entity_user_list_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_by_id_entity_user_get_by_id__id__get: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_entity_user_delete__id__delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_entity_user_enable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_enable_entity_user_enable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    disable_entity_user_disable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_disable_entity_user_disable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    count_entity_user_count_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_count_entity_user_count_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sum_entity_user_sum_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_sum_entity_user_sum_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    min_entity_user_min_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_min_entity_user_min_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    max_entity_user_max_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_max_entity_user_max_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    truncate_entity_user_truncate_delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    add_entity_instance_add_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_add_entity_instance_add_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_entity_instance_update_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_update_entity_instance_update_put"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_entity_instance_list_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_list_entity_instance_list_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_by_id_entity_instance_get_by_id__id__get: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_entity_instance_delete__id__delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_entity_instance_enable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_enable_entity_instance_enable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    disable_entity_instance_disable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_disable_entity_instance_disable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    count_entity_instance_count_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_count_entity_instance_count_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sum_entity_instance_sum_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_sum_entity_instance_sum_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    min_entity_instance_min_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_min_entity_instance_min_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    max_entity_instance_max_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_max_entity_instance_max_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    truncate_entity_instance_truncate_delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    add_entity_currency_add_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_add_entity_currency_add_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_entity_currency_update_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_update_entity_currency_update_put"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_entity_currency_list_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_list_entity_currency_list_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_by_id_entity_currency_get_by_id__id__get: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_entity_currency_delete__id__delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_entity_currency_enable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_enable_entity_currency_enable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    disable_entity_currency_disable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_disable_entity_currency_disable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    count_entity_currency_count_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_count_entity_currency_count_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sum_entity_currency_sum_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_sum_entity_currency_sum_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    min_entity_currency_min_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_min_entity_currency_min_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    max_entity_currency_max_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_max_entity_currency_max_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    truncate_entity_currency_truncate_delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    add_entity_broker_add_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_add_entity_broker_add_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_entity_broker_update_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_update_entity_broker_update_put"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_entity_broker_list_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_list_entity_broker_list_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_by_id_entity_broker_get_by_id__id__get: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_entity_broker_delete__id__delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_entity_broker_enable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_enable_entity_broker_enable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    disable_entity_broker_disable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_disable_entity_broker_disable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    count_entity_broker_count_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_count_entity_broker_count_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sum_entity_broker_sum_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_sum_entity_broker_sum_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    min_entity_broker_min_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_min_entity_broker_min_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    max_entity_broker_max_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_max_entity_broker_max_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    truncate_entity_broker_truncate_delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    add_entity_asset_add_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_add_entity_asset_add_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_entity_asset_update_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_update_entity_asset_update_put"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_entity_asset_list_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_list_entity_asset_list_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_by_id_entity_asset_get_by_id__id__get: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_entity_asset_delete__id__delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_entity_asset_enable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_enable_entity_asset_enable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    disable_entity_asset_disable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_disable_entity_asset_disable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    count_entity_asset_count_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_count_entity_asset_count_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sum_entity_asset_sum_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_sum_entity_asset_sum_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    min_entity_asset_min_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_min_entity_asset_min_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    max_entity_asset_max_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_max_entity_asset_max_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    truncate_entity_asset_truncate_delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    add_entity_account_group_add_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_add_entity_account_group_add_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_entity_account_group_update_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_update_entity_account_group_update_put"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_entity_account_group_list_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_list_entity_account_group_list_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_by_id_entity_account_group_get_by_id__id__get: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_entity_account_group_delete__id__delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_entity_account_group_enable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_enable_entity_account_group_enable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    disable_entity_account_group_disable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_disable_entity_account_group_disable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    count_entity_account_group_count_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_count_entity_account_group_count_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sum_entity_account_group_sum_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_sum_entity_account_group_sum_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    min_entity_account_group_min_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_min_entity_account_group_min_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    max_entity_account_group_max_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_max_entity_account_group_max_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    truncate_entity_account_group_truncate_delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    add_entity_account_add_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_add_entity_account_add_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    update_entity_account_update_put: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_update_entity_account_update_put"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    list_entity_account_list_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_list_entity_account_list_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    get_by_id_entity_account_get_by_id__id__get: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    delete_entity_account_delete__id__delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    enable_entity_account_enable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_enable_entity_account_enable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    disable_entity_account_disable__id__patch: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                id: number;
            };
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_disable_entity_account_disable__id__patch"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    count_entity_account_count_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: {
            content: {
                "application/json": components["schemas"]["Body_count_entity_account_count_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    sum_entity_account_sum_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_sum_entity_account_sum_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    min_entity_account_min_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_min_entity_account_min_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    max_entity_account_max_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["Body_max_entity_account_max_post"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
    truncate_entity_account_truncate_delete: {
        parameters: {
            query?: {
                instance?: string | null;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": unknown;
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
