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
        Planned End date for the Task
    """,
    'author': 'S4 Solutions, LLC',
    'website': 'https://www.sfour.io/',
    'sequence': 10,
    'category': 'Custom',
    'license': 'AGPL-3',
    'version': '15.0.1.0.0',
    'depends': [
        'sale_project',
        'sale_timesheet',
        'resource',
        'mrp',
        'stock',
    ],
    'data': [
        'views/project_task_views.xml',
        'views/mrp_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
