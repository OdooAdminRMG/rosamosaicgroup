# -*- coding: utf-8 -*-

{
    "name": "RMG Sales",
    "summary": """RMG Sales""",
    "description": """
            Manage Delivery Dates on Sale Order
            
            User Stories: 21, 24, 61, 58
            """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "business",
    "version": "15.0.2.0.3",
    "depends": ["sale_management", "sale_stock", 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "reports/rmg_delivery_slip.xml",
        "reports/rmg_sale_order_report.xml",
        "views/product_template.xml",
        "views/res_configuration.xml",
        "views/sale_order_view.xml",
        "wizard/sale_order_confirm_wiz_view.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
