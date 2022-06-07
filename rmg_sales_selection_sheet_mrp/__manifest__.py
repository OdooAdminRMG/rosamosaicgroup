# -*- coding: utf-8 -*-

{
    "name": "RMG Sales Selection Sheet MRP",
    "summary": """RMG Sales Selection Sheet MRP""",
    "description":
        """
            This module is created to prevent
            direct dependency  between 'RMG Sales Selection Sheet' 
            and 'RMG Manufacturing Customizations'
        """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "sales",
    "version": "15.0.0.1.0",
    "depends": ["rmg_sales_selection_sheet", "rmg_mrp"],
    "data": [
        "report/rmg_mrp_production_report.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
