# -*- coding: utf-8 -*-
{
    'name': "Rmg Document Preview",
    'summary': """
        Document Preview allows users to preview a document without downloading it that leads to saving
         time and storage of users.
        """,
    'description': """
        document preview app, 
    """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    'category': 'Tools',
    'version': '15.0.0.0.0',
    'depends': ['base', 'web', 'mail'],
    'data': [
            'views/users.xml',
        ],
    'assets': {
        'web.assets_backend': [
            '/rmg_binary_file_preview/static/src/js/rmg_binary_preview.js',
            '/rmg_binary_file_preview/static/src/js/widget/RmgListDocumentViewer.js',

        ],

        'web.assets_qweb': ['rmg_binary_file_preview/static/src/xml/rmg_binary_preview.xml',
                            'rmg_binary_file_preview/static/src/js/widget/RmgListDocumentViewer.xml',
                            ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 100,
}
