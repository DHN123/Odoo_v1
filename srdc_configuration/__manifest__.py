# -*-coding: utf-8 -*-
{
    'name': "SRDC Configuaration module",
    'summary': """Configuration module""",
    'version': '12.0.0.1',
    'description': """No disc""",
    'author': "NhiDo",
    'category': 'sale, qc, purchase_requisition',
    'depends': [
        'srdc_base', 'srdc_purchase_requisition', 'srdc_sale',
    ],
    'data': [
        # Data
        # Security (group - rule)
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        # Wizard
        # View
        'views/res_groups.xml',
        'views/srdc_uom_uom.xml',
        'views/srdc_user.xml',
        'views/srdc_vat.xml',
        # Menu
        'menu/menu.xml',
    ],
    "qweb":[

    ],
    'application': True,
}