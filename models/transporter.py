from odoo import models,fields,api

class Transporter(models.Model):
    _name = 'transport.transporter'
    _description = 'Transporter Details'
    _rec_name = 'company_name'

    company_name = fields.Char()
    contact_person = fields.Char(string="Contact Person")
    address = fields.Char(string="Address")
    phone_no = fields.Char('Phone No')
    mobile_no = fields.Char('Mobile No')
    email = fields.Char('Email')
    logo = fields.Binary("Logo")
    delivery_count = fields.Integer(string="Delivery Count",compute="_compute_delivery_count")
    vehicle_count = fields.Integer(string='Vehicle Count',compute="_compute_vehicle_count")


    def _compute_delivery_count(self):
        for transporter in self:
            # Assuming 'your_field_to_link_to_picking' is a reference to stock.picking model, like a one2many or many2many relation
            transporter.delivery_count = self.env['stock.picking'].search_count([
                ('transport_id', '=', transporter.id)
            ])

    def action_view_deliveries(self):
        self.ensure_one()
        # Show the related stock.picking records
        return {
            'name': 'All Deliveries',
            'domain': [('transport_id', '=', self.id)],  # Adjust domain if you use a different relation
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'context': {'default_transport_id': self.id},
        }

    def _compute_vehicle_count(self):
        for transporter in self:
            transporter.vehicle_count = self.env['transport.vehicle'].search_count([
                ('transporter_id', '=', transporter.id)  # Adjust this to your transporter relation field
            ])

    def action_view_vehicle(self):
        self.ensure_one()
        return {
            'name': 'Vehicles',
            'domain': [('transporter_id', '=', self.id)],  # Adjust this domain if needed
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'transport.vehicle',
            'type': 'ir.actions.act_window',
            'context': {'default_transporter_id': self.id},
        }
