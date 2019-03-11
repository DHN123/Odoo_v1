# -*- coding: utf-8 -*-

{
    'name': "SRDC (Theme)",
    "summary": "Theme for SRDC in Odoo v12",
    "author": "CongDPT",
    "category": "web",
    'version': '12.0.0.1',
    "license": "LGPL-3",
    "depends": [],
    "data": [
        'views/assets.xml',
        'views/sidebar.xml',
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/web.xml",
    ],
    "images": ['static/description/icon.jpg'],
    'installable': True,
    'application': True,
    'auto_install': False,

}
