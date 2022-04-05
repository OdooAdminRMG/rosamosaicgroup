# -*- coding: utf-8 -*-
{
    "name": "RMG MRP",
    "version": "15.0.1.1",
    "sequence": 22,
    "summary": "Custom RMG MRP",
    "description": """
        Custom RMG MRP
    """,
    "depends": ["mrp"],
    "data": [
        "views/mrp_production_view.xml",
        "report/rmg_mrp_order_report.xml",
        "report/mrp_report_rmg_mrp.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
