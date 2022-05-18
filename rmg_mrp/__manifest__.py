# -*- coding: utf-8 -*-
{
    "name": "RMG Manufacturing Customizations",
    "description": "",
    "category": "sales",
    "summary": "",
    "sequence": 20,
    "version": "15.0.1.2.0",
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    "depends": ["stock", "sale_management", "mrp"],
    "data": [
        "views/product_view.xml",
        "views/stock_picking_type.xml",
        "views/mrp_production_view.xml",
        "report/rmg_mrp_order_report.xml",
        "report/mrp_report_rmg_mrp.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
