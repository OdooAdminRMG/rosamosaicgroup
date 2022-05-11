# -*- coding: utf-8 -*-

{
    "name": "RMG CRM",
    "summary": """RMG CRM""",
    "description": """RMG CRM""",
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "sales",
    "version": "15.0.2.2.1",
    "depends": ["sale_management", "sale_crm", "project", "stock", "purchase", "mrp"],
    "data": [
        "views/rmg_sale_views.xml",
        "views/rmg_mrp_views.xml",
        "views/rmg_project_views.xml",
        "views/rmg_stock_picking_views.xml",
    ],
    'assets': {
        'web.assets_qweb': [
            # 'rmg_crm/static/src/xml/web_calendar.xml',
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
