# -*-coding: utf-8 -*-
{
    'name': "SRDC Purchase module",
    'summary': """Purchase module""",
    'version': '12.0.0.1',
    'description': """No disc""",
    'author': "NhiDo",
    'category': 'sale, qc',
    'depends': [
        'srdc_base',
    ],
    'data': [
        # Data
        'data/srdc_purchase_data.xml',
        # Security (group - rule)
        # 'security/purchase_user.xml',
        'security/ir.model.access.csv',
        # Wizard
        # View
        'views/srdc_purchase_order.xml',
        'views/srdc_purchase_attribute.xml',
        'views/srdc_purchase_attribute_value.xml',
        # Menu
        'menu/menu.xml',
    ],
    "qweb":[

    ],
    'application': True,
}
