# -*- coding: utf-8 -*-
{
    "name": "RMG Adjust Stock Valuation",
    "description":
        """
            RMG Adjust Stock Valuation
            
            Tasks: 'Update MO costing report source data', 
            User Stories:
        """,
    "category": "sales",
    "summary": "",
    "sequence": 20,
    "version": "15.0.0.1.0",
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    "depends": ["rmg_stock","stock","stock_account"],
    "data": [
        "views/stock_valuation_layer_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
