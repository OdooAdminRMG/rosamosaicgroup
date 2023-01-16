# -*- coding: utf-8 -*-
{
    'name': "Edit Stock Quant reserve Qty Base",
    'summary': """Used to edit reserve quantity.""",
    'description': """Used to edit reserve quantity.""",
    'author': 'S4 Solutions, LLC',
    'website': 'https://www.sfour.io/',
    'category': 'stock',
    'version': '15.0.1.0.0',
    'depends': ['stock'],
    'data': [
        'security/stock_security.xml',
        'security/ir.model.access.csv',
        'views/stock_quant_views.xml',
        'wizard/edit_stock_quant_wizard.xml',
    ],
}
