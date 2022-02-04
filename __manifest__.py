# -*- coding:utf-8 -*-

{
	'name' : 'Budget Import and Export in Excel',
	'version': '1.1.1',
    'author' : 'Probuse Consulting Service Pvt. Ltd.',
    'website' : 'www.probuse.com',
	    'price': 29.0,

    'currency': 'EUR',
    'license': 'Other proprietary',
	'category': 'Accounting',
	'summary':  """This app allow you to import and export budget from excel format file.""",
	'description': """
Import Budget Line from Excel
Export Budget In Excel  
budget
account budget
budget excel
Budget Import and Export in Excel
import budget
This app allow you to import and export budget from excel format file.
export budget
    """,
    'images': ['static/description/img1.jpg'],
    #'live_test_url': 'https://youtu.be/KHHgKKKDnso',
    'external_dependencies': {'python': ['xlrd']},
	'depends': ['om_account_budget'],
	'data': [
	    'wizard/budget_line_import.xml',
	    'wizard/budget_export.xml',
		'views/budget_import_view.xml',
	],
	'installable' : True,
	'application' : True,
}



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 

