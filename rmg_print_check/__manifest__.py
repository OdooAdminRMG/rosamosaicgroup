# -*- coding: utf-8 -*-
{
    "name": "RMG Print Check",
    "description": "RMG Print Check",
    "category": "Accounting/Localizations/Check",
    "summary": "RMG Print Check",
    "sequence": 20,
    "version": "15.0.0.3.0",
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    "depends": ["l10n_us_check_printing",],
    "data": [
        "reports/print_check_middle_template.xml",
    ],
    'assets': {
        'web.report_assets_common': [
            'rmg_print_check/static/**/*',
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
