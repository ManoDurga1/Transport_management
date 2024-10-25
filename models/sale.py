from odoo import models,fields,api

class Sale(models.Model):
    _inherit = 'sale.order'

    transport_id = fields.Many2one(related='transporter_route.transporter_id',string="Transport By")
    transporter_route = fields.Many2one('transport.routes',string="Transporter Route")



