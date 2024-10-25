from odoo import models,fields,api
from odoo.exceptions import UserError


class TransportLocations(models.Model):
    _name = 'transport.locations'
    _description = 'Transport Locations'
    _rec_name = 'location'

    location = fields.Char(string='Locations')



class LocationDetails(models.Model):
    _name = 'location.details'
    _description = 'Transport Location Details'

    # this route_id is a field to link to the location_route_ids  filed to create the location details in transport.routes model
    route_id = fields.Many2one('transport.routes', string='Routes')
    start_location_id = fields.Many2one('transport.locations', string='Start Location')
    end_location_id = fields.Many2one('transport.locations', string='End Location')
    distance = fields.Float(string='Distance (km)')
    transport_charges = fields.Float(string='Transport Charge')
    time = fields.Float(string="Time")


    # this page_id is a field to link to the transport_page_ids  filed to create the transport route details in stock.picking model
    page_id = fields.Many2one('stock.picking',string='Page')
    demo_id = fields.Many2one('transport.entry')
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')

    tracking_num = fields.Char(string='Tracking Number')
    state = fields.Selection([('start', 'Start'), ('waiting', 'Waiting'), ('in-progress', 'In-Progress'),
                              ('done', 'Delivered'), ('cancel', 'Cancelled')], default='start', string="State"
                            )

    # @api.model
    # def create(self,vals):
    #     for rec in self.page_id.transport_entry_ids:
    #         vals['tracking_num'] = rec.name
    #         print("helloooo")
    #     return super(LocationDetails, self).create(vals)





