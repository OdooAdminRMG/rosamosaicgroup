# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software PVT. LTD.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.


{
    'name': 'RMG Manufacturing Projects',
    'summary': """
        RMG Manufacturing Project
    """,
    'description': """
        RMG Manufacturing Project module helps user to set templator and project manager
        from project and task.
        
        User Stories: 60
    """,
    'author': 'S4 Solutions, LLC',
    'website': 'https://www.sfour.io/',
    'sequence': 10,
    'category': 'Custom',
    'license': 'AGPL-3',
    'version': '15.0.0.0.0',
    'depends': [
        'project',
        'mrp',
        'rmg_mrp'
    ],
    'data': [
        'views/mrp_views.xml',
        'reports/rmg_mrp_production_reprt.xml',
    ],
    'installable': True,
    'auto_install': False,
}
