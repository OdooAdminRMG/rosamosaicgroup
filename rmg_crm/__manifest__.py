# -*- coding: utf-8 -*-


{
    "name": "RMG CRM",
    "summary": """RMG CRM""",
    "description": """
        RMG CRM
        
        Important: 
            1. Run "Update Job Name In Existing Invoices" manually 
               to update sale id of those invoices which are created 
               before installation of this module. (only need to run it once 
               while deploying this module)
            2. Run "Create Replenish Sources History For Existing PO" manually 
               to update replenish history of those POs which are created 
               before installation of this module. (only need to run it once 
               while deploying this module)
            
            User Stories: 11, 15, 26, 44, 
            Task: 
                1. Daniel Grider Project App Access
    """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "sales",
    "version": "15.0.5.23.12",
    "depends": [
        "sale_management",
        "sale_crm",
        "project",
        "stock",
        "purchase",
        "mrp",
        "timesheet_grid",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/update_attachments.xml",
        "data/job_costing_report_filter.xml",
        "data/create_replenish_sources_history_for_existing_po.xml",
        "data/update_job_name_in_existing_invoices.xml",
        "views/attachment_type_views.xml",
        "views/ir_attachment_views.xml",
        "views/crm_views.xml",
        "views/rmg_sale_views.xml",
        "views/rmg_mrp_views.xml",
        "views/rmg_project_views.xml",
        "views/rmg_stock_picking_views.xml",
        "views/replenish_source_views.xml",
        "views/purchase_order_views.xml",
        "views/account_move_views.xml",
        "views/job_costing_views.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "rmg_crm/static/src/xml/filter_menu.xml"
            # 'rmg_crm/static/src/xml/web_calendar.xml',
        ],
        "web.assets_backend": ["rmg_crm/static/src/js/search_utils.js"],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
