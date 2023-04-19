# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

{
    "name": "RMG Project Enhancements",
    "summary": """RMG Project Enhancements""",
    "description": """
            RMG Project Enhancements
            
            User Stories: 20, 41, 47, 66,
            """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "business",
    "version": "15.0.3.1.0",
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
    'assets': {
        'web.assets_backend': [
            'rmg_project/static/src/js/project_calendar.js',
            ]},
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
