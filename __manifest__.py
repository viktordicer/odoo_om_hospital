# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'summary': 'Hospital management system',
    'description': """Hospital management system""",
    'depends': ['mail', 'product',],
    'data': [
        'security/ir.model.access.csv',
        'data/om_hospital_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/patient_tag_view.xml',
        'views/appointment_view.xml',
        'views/female_patient_view.xml',
        ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
