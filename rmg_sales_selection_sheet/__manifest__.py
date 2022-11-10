# -*- coding: utf-8 -*-

{
    "name": "RMG Sales Selection Sheet",
    "summary": """RMG Sales Selection Sheet""",
    "description": """
    
        RMG Sales Selection Sheet
        
        User Stories: 2, 7, 
    """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "sales",
    "version": "15.0.2.9.6",
    "depends": ["sale_management", "stock", "purchase", "mrp", "hr_recruitment"],
    "data": [
        "data/edge_profiles_data.xml",
        "data/customer_sink_types_data.xml",
        "data/corner_treatments_data.xml",
        "data/faucets_data.xml",
        "data/range_types_data.xml",
        "security/ir.model.access.csv",
        "views/add_product_views.xml",
        "views/selection_sheet_configuration.xml",
        "views/edge_profiles_views.xml",
        "views/mrp_production_views.xml",
        "views/customer_sink_types_views.xml",
        "views/faucets_views.xml",
        "views/corner_treatments_views.xml",
        "views/range_types_views.xml",
        "views/rmg_sale_views.xml",
        "wizard/rmg_sale_warning_wiz_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "rmg_sales_selection_sheet/static/src/js/section_and_note_fields_backend.js",
            "rmg_sales_selection_sheet/static/src/js/section_form.js",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
