from odoo import models,fields,api

class TransportRoutes(models.Model):
    _name = 'transport.routes'
    _description = 'Transport Routes'
    _rec_name = 'route_name'

    route_name = fields.Char(string="Route Name" , compute="_compute_route")
    transporter_id = fields.Many2one('transport.transporter', string='Transporter')
    location_route_ids = fields.One2many('location.details','route_id')

    @api.depends('location_route_ids')
    def _compute_route(self):
        for record in self:
            if record.location_route_ids:
                first_route = record.location_route_ids[0]  # Get the first route in the One2many field
                if first_route.start_location_id and first_route.end_location_id:
                    # Concatenate start and end location names to form the route name
                    record.route_name = f"{first_route.start_location_id.location} - {first_route.end_location_id.location}"
                else:
                    record.route_name = "Specify the  Route"
            else:
                record.route_name = "Specify the Route"