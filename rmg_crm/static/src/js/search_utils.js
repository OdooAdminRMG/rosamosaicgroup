/* @odoo-module */

//odoo.define('rmg_crm.rmg_custom_search_filter', function(require) {
//"use strict";

    const { _lt, _t } = require('web.core');
    var {FIELD_OPERATORS} = require('web.searchUtils');
    FIELD_OPERATORS['datetime'] = [
                { symbol: "<=", description: _lt("is before or equal to") },
                { symbol: "between", description: _lt("is between") },
                { symbol: "=", description: _lt("is equal to") },
                { symbol: "!=", description: _lt("is not equal to") },
                { symbol: ">", description: _lt("is after") },
                { symbol: "<", description: _lt("is before") },
                { symbol: ">=", description: _lt("is after or equal to") },
                { symbol: "!=", description: _lt("is set"), value: false },
                { symbol: "=", description: _lt("is not set"), value: false },
            ]
//});
