{
    'name' : 'Transport Management System',
    'version' : '17.01',
    'category' : 'Transport',
    'summery' : 'Manage transport vehicles, locations, routes',
    'author' : 'Mr.Manu',
    'depends' : [
        'base',
        'sale',
        'fleet',
        'stock',
    ],
    'data' : [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/transport_vehicle.xml",
        "views/transporter.xml",
        "views/menu.xml",
        "views/transport_locations.xml",
        "views/transport_routes.xml",
        "views/sale.xml",
        "views/inventory_stock.xml",
        "views/transport_entry.xml",
        "report/transport_entry_report.xml",
        "report/transport_entry_template.xml",
        "report/report_deliveryslip.xml",


    ]
}