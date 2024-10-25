from odoo import models,fields,api

class TransportEntry(models.Model):
    _name = 'transport.entry'
    _inherit = ['mail.thread']
    _description = 'Transport Entry Details'

    name = fields.Char()
    customer_id = fields.Many2one('res.partner',string='Customer')
    transport_date = fields.Date(string='Transport Date')
    delivery_order_id = fields.Many2one('stock.picking',string='Delivery Order')
    lr_number = fields.Char(string='LR Number')
    transport_id = fields.Many2one('transport.transporter', string="Transport By", readonly=True)
    contact_person = fields.Char(string="Contact Person")
    no_of_parcels = fields.Integer(string='No Of Parcels')
    vehicle_id = fields.Many2one('fleet.vehicle',string='Transport Vehicle')
    state = fields.Selection([('start','Start'),('waiting','Waiting'),('in-progress','In-Progress'),
                              ('done','Delivered'),('cancel','Cancelled')],default='start',string="State", track_visibility='onchange')

    # location details
    # Many2one field to select the route
    route_id = fields.Many2one('transport.routes', string="Route", required=True)

    # One2many field to fetch location details from location.details model, via transport.routes
    location_route_ids = fields.One2many('location.details','demo_id',string="Location Details")


    # this entry_id is linked to the One2many field in stock.picking model to create the page in that model
    entry_id = fields.Many2one('stock.picking',string='Entry')

    tracking_num = fields.Char(string='Tracking Number')

    @api.model
    def create(self, vals):
        record = super(TransportEntry, self).create(vals)

        # Fetch the related location details from the selected route
        if record.route_id and record.route_id.location_route_ids:
            # Create independent copies of location details for this transport entry
            new_location_details = []
            for location in record.route_id.location_route_ids:
                new_location_details.append((0, 0, {
                    'start_location_id': location.start_location_id.id,
                    'end_location_id': location.end_location_id.id,
                    'distance': location.distance,
                    'transport_charges': location.transport_charges,
                    'time': location.time,
                    # 'start_time': location.start_time,
                    # 'end_time': location.end_time,
                    'tracking_num': location.tracking_num,
                    'state': 'start'  # Ensure the state starts as 'start'
                }))
            # Now, update the transport entry record with the new location details
            record.write({'location_route_ids': new_location_details})

        return record

    def action_start(self):
        self.state = 'in-progress'
        for location in self.location_route_ids:
            location.start_time = fields.Datetime.now()
        self._update_location_state('in-progress')  # Update related location details
        self._populate_transport_location_details()
    def action_waiting(self):

        self.state = 'waiting'
        self._update_location_state('waiting')  # Update related location details
        self._populate_transport_location_details()

    def action_cancel(self):

        self.state = 'cancel'
        self._update_location_state('cancel')  # Update related location details
        self._populate_transport_location_details()

    def action_done(self):

        self.state = 'done'
        for location in self.location_route_ids:
            location.end_time = fields.Datetime.now()
        self._update_location_state('done')  # Update related location details
        self._populate_transport_location_details()

    # Custom method to update state in related location details
    def _update_location_state(self, new_state):
        for location in self.location_route_ids:
            location.state = new_state


    # The details from the transport entry ->transport.location.details populated into stock->transport.location.details

    def _populate_transport_location_details(self):
        """ Populate transport location details in stock picking """
        if self.entry_id:
            picking = self.entry_id
            # Clear existing location details in stock.picking
            picking.transport_page_ids = [(5, 0, 0)]  # Clears all One2many records

            # Add location details from transport.entry to stock.picking
            for location_detail in self.location_route_ids:
                picking.transport_page_ids = [(0, 0, {
                    'start_location_id': location_detail.start_location_id.id,
                    'end_location_id': location_detail.end_location_id.id,
                    'distance': location_detail.distance,
                    'transport_charges': location_detail.transport_charges,
                    'time': location_detail.time,
                    'start_time': location_detail.start_time,
                    'end_time': location_detail.end_time,
                    'tracking_num': location_detail.tracking_num,
                    'state': location_detail.state,

                })]













