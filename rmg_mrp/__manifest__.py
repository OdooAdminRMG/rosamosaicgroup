# -*- coding: utf-8 -*-
{
    "name": "RMG Manufacturing Customizations",
    "description": """
            User Stories: 5, 22, 48, 
    """,
    "category": "sales",
    "summary": "",
    "sequence": 20,
    "version": "15.0.2.7.2",
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    "depends": ["stock", "sale_management", "mrp"],
    "data": [
        "data/create_records_for_existing_data.xml",
        "security/ir.model.access.csv",
        "views/quants_locations.xml",
        "views/product_view.xml",
        "views/stock_views.xml",
        "views/stock_picking_type.xml",
        "views/mrp_production_view.xml",
        "report/rmg_mrp_order_report.xml",
        "report/mrp_report_rmg_mrp.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
