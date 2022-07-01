# -*- coding: utf-8 -*-
{
    "name": "RMG Inventory Management",
    "description":
        """
            RMG Inventory Management
            
            Tasks: 'Update MO costing report source data', 
            User Stories:
        """,
    "category": "sales",
    "summary": "",
    "sequence": 20,
    "version": "15.0.0.0.0",
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    "depends": ["stock","stock_account"],
    "data": [
        "views/inventory_configurations_view.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
