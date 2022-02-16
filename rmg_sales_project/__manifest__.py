# -*- coding: utf-8 -*-

{
    'name': "RMG Sales Project",
    'summary': """
        RMG Sales Project""",
    'description': """
        RMG Sales Project module helps user to set Lead time on Task and calculated Planned Start date and 
        Planned End date for the Task""",
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'sequence': 10,
    'category': 'Custom',
    'license': 'AGPL-3',
    'version': '15.0.1.0.0',
    'depends': [
        'sale_project'
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'views/project_task_views.xml',
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,

}
