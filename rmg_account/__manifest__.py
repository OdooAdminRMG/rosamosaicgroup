# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

{
    "name": "RMG Account",
    "summary": """RMG Account""",
    "description": """Manage Account""",
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "business",
    "version": "15.0.3.0.1",
    "depends": ["account_reports","stock_account"],
    "data": [
        "views/product_category_view.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
