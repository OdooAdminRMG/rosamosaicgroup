# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Multi Sale Order Cancel',
    'version' : '1.0',
    'author':'Craftsync Technologies',
    'category': 'Sales',
    'maintainer': 'Craftsync Technologies',
    'summary': "Enable mass cancel order workflow with cancel sale order automation. Include operations like Auto Invoice Cancel, Auto Cancel Delivery Order. Even if invoice was paid and delivery was transfered. unreconcile payment of paid invoice. Now user can select multi sale order cancel",
    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'depends' : ['cancel_sale_order'],
    'data': [
       'security/ir.model.access.csv',
       'views/view_cancel_multi_order.xml',
    ],    
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'price': 5.00,
    'currency': 'USD',

}
