{
    'name': "Library Management",

    'summary': "Gestión de Biblioteca y Préstamos",

    'description': """
        Este módulo de gestión de biblioteca para Odoo permite a los usuarios gestionar libros, autores, préstamos y devoluciones de manera eficiente. Con este módulo, los bibliotecarios pueden mantener un registro de los libros disponibles, gestionar las reservas y controlar el estado de los préstamos. Además, los usuarios pueden buscar libros, realizar reservas y consultar su historial de préstamos. Este módulo es ideal para bibliotecas escolares, públicas o privadas que desean mejorar su gestión y ofrecer una mejor experiencia a sus usuarios.
    """,

    'author': "Patrick_Guardado",
    #'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],
    
    # always loaded
    
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/book_views.xml',
        'views/views.xml',
        #'views/templates.xml',
    ],
    
    'application': True,
    'installable': True,
    #'auto_install': False,
    

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

