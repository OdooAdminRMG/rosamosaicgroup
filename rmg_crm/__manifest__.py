# -*- coding: utf-8 -*-


{
    "name": "RMG CRM",
    "summary": """RMG CRM""",
    "description": """RMG CRM""",
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "sales",
    "version": "15.0.3.16.4",
    "depends": ["sale_management", "sale_crm", "project", "stock", "purchase", "mrp", "timesheet_grid"],
    "data": [
        "security/ir.model.access.csv",
        "data/create_replenish_sources_history_for_existing_po.xml",
        "views/attachment_type_views.xml",
        "views/ir_attachment_views.xml",
        "views/crm_views.xml",
        "views/rmg_sale_views.xml",
        "views/rmg_mrp_views.xml",
        "views/rmg_project_views.xml",
        "views/rmg_stock_picking_views.xml",
        "views/replenish_source_views.xml",
        "views/purchase_order_views.xml",
        "views/job_costing_views.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            # 'rmg_crm/static/src/xml/web_calendar.xml',
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
