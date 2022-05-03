# -*- coding: utf-8 -*-

{
    "name": "RMG Sales",
    "summary": """RMG Sales""",
    "description": """Manage Delivery Dates on Sale Order""",
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "business",
    "version": "15.0.2.0.1",
    "depends": ["sale_management", "sale_stock", 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "reports/rmg_delivery_slip.xml",
        "views/inventory_configuration.xml",
        "views/sale_order_view.xml",
        "wizard/sale_order_confirm_wiz_view.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
