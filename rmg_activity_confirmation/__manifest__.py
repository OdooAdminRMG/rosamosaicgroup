# -*- coding: utf-8 -*-
{
    "name": "RMG Activity Confirmation",
    "description":
        """
            RMG Activity Confirmation
            
            Tasks: 'E-mail Confirmation on Activity Completion',
            User Stories:59
        """,
    "category": "Productivity/Discuss",
    "summary": "",
    "sequence": 20,
    "version": "15.0.0.0.1",
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    "depends": ["mail"],
    "data": [
        "data/activity_confirmation_mail.xml",
        "views/mail_activity_views.xml",
    ],
    'web.assets_backend': [
        'rmg_activity_confirmation/static/src/js/activity.js',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
