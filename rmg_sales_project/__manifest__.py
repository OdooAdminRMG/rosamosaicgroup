# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software PVT. LTD.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
#   Aktiv Software:
#       - Isufi Kapasi

{
    'name': 'RMG Sales Projects',
    'summary': """
        RMG Sales Project
    """,
    'description': """
        RMG Sales Project module helps user to set Lead time on Task and calculated Planned Start date and 
        Planned End date for the Task.
        
        User Stories: 1, 3, 9, 53, 52, 51, 57, 
    """,
    'author': 'S4 Solutions, LLC',
    'website': 'https://www.sfour.io/',
    'sequence': 10,
    'category': 'Custom',
    'license': 'AGPL-3',
    'version': '15.0.4.3.3',
    'depends': [
        'project',
        'project_enterprise',
        'rmg_crm',
        'rmg_sales_selection_sheet',
        'sale_project',
        'sale_timesheet',
        'resource',
        'mrp',
        'stock',
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'views/sale_order_view.xml',
        'views/project_task_views.xml',
        'views/mrp_views.xml',
        'views/stock_picking_views.xml',
        "reports/rmg_quotation_report.xml",
    ],
    'assets': {
        'web.assets_qweb': [
            'rmg_sales_project/static/src/xml/web_calendar.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
}
