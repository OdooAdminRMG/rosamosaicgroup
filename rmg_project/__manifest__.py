# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

{
    "name": "RMG Project Enhancements",
    "summary": """RMG Project Enhancements""",
    "description": """RMG Project Enhancements""",
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "business",
    "version": "15.0.2.0.2",
    "depends": [
        "sale_project",
        "calendar"
    ],
    "data": [
        "views/project_view.xml",
        "views/sale_order_view.xml",
        "views/menu_view.xml",
        "views/project_stages.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
