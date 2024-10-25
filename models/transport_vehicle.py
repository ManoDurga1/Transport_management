from odoo import models,fields,api

class TransportVehicle(models.Model):
    _name = 'transport.vehicle'
    _description = 'Transport Vehicle'
    _rec_name = 'vehicle_id'


    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle Name')
    model_id = fields.Many2one('fleet.vehicle.model', related='vehicle_id.model_id',string='Model')
    license_id = fields.Char(related='vehicle_id.license_plate',string='License Plate')
    vehicle_type = fields.Many2one(related='vehicle_id.category_id', string='Vehicle Type')
    capacity = fields.Float('Capacity (in tons)')
    driver_id = fields.Many2one('res.partner', related='vehicle_id.driver_id', string='Driver')
    status = fields.Many2one(
        related='vehicle_id.state_id',
        string="Status")

    transporter_id = fields.Many2one('transport.transporter', string='Transporter')


