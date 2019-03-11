# -*-coding: utf-8 -*-
{
    'name': "SRDC Sale",
    'summary': """Sales module""",
    'version': '12.0.0.1',
    'description': """No disc""",
    'author': "CongDPT, Nhi Do",
    'category': 'sale',
    'depends': [
        'partner_autocomplete',
        'project',
        'sale_management',
        'srdc_qc',
    ],
    'data': [
        # Data
        'data/concrete_product_category.xml',
        'data/ir_config_parameter.xml',
        'data/product_attribute_category.xml',
        'data/res_company.xml',
        'data/res_partner.xml',
        # Security ( group - rule)
        'security/ir.model.access.csv',
        # Wizard
        'wizards/wizard_generate_io.xml',
        'wizards/wizard_request_qc.xml',
        # View
        'views/product_category.xml',
        'views/product_template.xml',
        'views/project_competitor.xml',
        'views/project_customer.xml',
        'views/sale_order.xml',
        'views/project_project.xml',
        'views/project_project_input.xml',
        'views/project_report.xml',
        'views/res_company.xml',
        'views/res_country_district.xml',
        'views/srdc_concrete_pump_category.xml',
        'views/srdc_concrete_pump_volume.xml',
        'views/srdc_contract.xml',
        'views/srdc_floor_elevation.xml',
        'views/srdc_io.xml',
        'views/res_country_ward.xml',
        'views/res_partner.xml',
        'views/srdc_tender_package.xml',
        'views/srdc_type_of_pump.xml',
        # Menu
        'menu/menu.xml'
    ],
    "qweb": [
        # "static/src/xml/qweb.xml",
    ],
    'application': True,
}
