# -*-coding: utf-8 -*-
{
    'name': "SRDC QC",
    'summary': """QC module""",
    'version': '12.0.0.1',
    'description': """No disc""",
    'author': "CongDPT",
    'category': 'sale',
    'depends': [
        'purchase',
        'srdc_base',
    ],
    'data': [
        # Data
        'data/product_category.xml',
        'data/product_template.xml',
        'data/srdc_trialmix_result_value.xml',
        # Security ( group - rule)
        'security/ir.model.access.csv',
        # Wizard
        # View
        'views/product_supplierinfo.xml',
        'views/product_template.xml',
        'views/res_company.xml',
        'views/srdc_mix_design.xml',
        'views/srdc_mix_procedure.xml',
        'views/srdc_trial_mix.xml',
        'views/srdc_trialmix_result_value.xml',
        # Menu
        'menu/menu.xml'
    ],
    'application': True,
}
