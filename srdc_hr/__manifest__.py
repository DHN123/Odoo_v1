# -*-coding: utf-8 -*-
{
    'name': "SRDC HR module",
    'summary': """HR module""",
    'version': '12.0.0.1',
    'description': """No disc""",
    'author': "NhiDo",
    'category': 'srdc_base, srdc_purchase_requisition, srdc_configuration, srdc_qc, srdc_sale',
    'depends': [
        'srdc_base', 'srdc_purchase_requisition', 'srdc_configuration', 'srdc_qc', 'srdc_sale',
    ],
    'data': [
        # Data

        # Security (rule - group)
        'security/ir.model.access.csv',
        # Wizard

        # View
        'views/srdc_hr_configuration_employees_tags.xml',
        'views/srdc_hr_configuration_setting.xml',
        'views/srdc_hr_department.xml',
        'views/srdc_hr_employee_status.xml',
        'views/srdc_hr_employees.xml',
        # Menu
        'menu/menu.xml',
    ],
    'qweb': [

    ],
    'application': True,
}