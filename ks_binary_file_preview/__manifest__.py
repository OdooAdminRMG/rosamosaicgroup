# -*- coding: utf-8 -*-
{
    'name': "Document Preview",

    'summary': """
        Document Preview allows users to preview a document without downloading it that leads to saving
         time and storage of users.
        """,

    'description': """
        Best Odoo Document Preview Apps
        Odoo Document Preview Apps
        Document Preview Apps
        Odoo Documents Preview Apps
        Documents Preview Apps
        Odoo Preview Document Apps
        Preview Document Apps
        View Document Apps
        Odoo View Document Apps
        Document View Apps
        Display Document Preview Apps
        Odoo Display Document Preview Apps
        PDF Document Preview Apps
        Odoo PDF Document Preview Apps
        Video Document Preview Apps
        Odoo Video Document Preview Apps
        Image Document Preview Apps
        Show Document Apps
        Binary Preview Apps
        Binary File Preview Apps
        File Preview Apps
        Show File Document
        Display Birany Files
        Show Attachment Files
        Display Attachment Files
        Display Files
        Check PDF Files
        Check File
        Check Image
        Document Checker
        File Checker
        Report Preview
        Odoo Report Preview
        Document Management System
        Document Management Portal
        Document Preview Portal
        Document Views In Website Portal
        Document Version
        Document Extension
        Document Viewer PDF
        MuK Documents View
        Asset Documents Management,
        document preview, 
        odoo document preview, 
        odoo document preview app, 
        odoo document module, 
        pdf preview, 
        pdf preview in odoo, 
        document preview tools, 
        pdf attachment preview, 
        odoo preview app, 
        employee documnet preview, 
        preview thumdnail, 
        preview thumbnail view, 
        document module
    """,

    'author': "Ksolves India Ltd.",

    'license': 'LGPL-3',

    'currency': 'EUR',

    'price': '0.0',

    'website': "https://store.ksolves.com/",

    'category': 'Tools',

    'support': 'sales@ksolves.com',

    'images': ['static/description/banners/banner1.gif'],

    'version': '15.0.1.0.2',

    'depends': ['base', 'web', 'mail'],

    'data': [
            'views/ks_user.xml',
        ],

    'assets': {
        'web.assets_backend': [
            '/ks_binary_file_preview/static/src/js/ks_binary_preview.js',
            '/ks_binary_file_preview/static/src/js/widget/ksListDocumentViewer.js',

        ],

        'web.assets_qweb': ['ks_binary_file_preview/static/src/xml/ks_binary_preview.xml',
                            'ks_binary_file_preview/static/src/js/widget/ksListDocumentViewer.xml',
                            ],
    },
}
