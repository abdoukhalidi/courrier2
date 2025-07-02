# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'axa_mail_tracking',
    'version': '1.0',
    'category': 'BO',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'website': 'https://www.odoo.com/app/crm',
    'depends': [
        'base',
    ],
    'data': [
        'security/axa_mail_tracking_security.xml',
        'security/ir.model.access.csv',



        'views/reporting_views.xml',
        'views/courier_views.xml',

    ],

    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'axa_mail_tracking/static/src/components/**',
            'axa_mail_tracking/static/src/xml/**',

        ],

    },
    'license': 'LGPL-3',
}
