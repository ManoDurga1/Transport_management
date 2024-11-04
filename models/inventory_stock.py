from odoo import models,fields,api

class InventoryStock(models.Model):
    _inherit = 'stock.picking'


    transport_id = fields.Many2one('transport.transporter',string="Transport By" ,readonly=True)
    transporter_route = fields.Many2one('transport.routes',string="Transporter Route",readonly=True)
    lr_number = fields.Char(string="LR Number")
    no_of_parcels = fields.Integer(string="No Of Parcels", compute='_compute_no_of_parcels')
    tracking_num = fields.Char(string="Tracking Number")

   #  creating a transport route page in stock.picking which is linked to the transport.locations
    transport_page_ids = fields.One2many('location.details','page_id')
    #  creating a transport entry page in stock.picking which is linked to the transport.entry model
    transport_entry_ids = fields.One2many('transport.entry', 'entry_id')

    def _compute_no_of_parcels(self):
        for picking in self:
            sale_order=picking.sale_id
            total_qty = 0  # Initialize total quantity
            if sale_order:
                for line in sale_order.order_line:
                    total_qty += line.product_uom_qty  # Add the quantity of each line
                picking.no_of_parcels = total_qty
            else:
                picking.no_of_parcels = 0

    @api.model
    def create(self, vals):
        # Check if the picking has a related sale order (through the origin field)
        if vals.get('origin'):
            # search the sale order
            sale_order = self.env['sale.order'].search([('name','=',vals['origin'])],limit=1)
            if sale_order:
                if sale_order.transporter_route:
                    vals['transporter_route'] = sale_order.transporter_route.id
                if sale_order.transport_id:
                    # Copy the "Transport by" field from Sale Order to Picking
                    vals['transport_id'] = sale_order.transport_id.id

        if vals.get('tracking_num', 'New') == 'New':
            vals['tracking_num'] = self.env['ir.sequence'].next_by_code('stock.picking') or 'New'

        return super(InventoryStock, self).create(vals)


    def button_validate(self):
        # Call the original button_validate method to proceed with validation
        res = super(InventoryStock, self).button_validate()
        for rec in self:
            # Fetch the transporter details using company_name
            transporter = self.env['transport.transporter'].search(
                [('company_name', '=', rec.transport_id.company_name)],limit=1) if rec.transport_id else False

                # Fetch the relevant data and create a transport entry
            transport_entry_vals = {
                'name' : rec.tracking_num,
                'delivery_order_id' : rec.id,
                'customer_id' : rec.partner_id.id,
                'transport_date' : rec.scheduled_date,
                'lr_number' : rec.lr_number,
                'transport_id' : rec.transport_id.id,
                'no_of_parcels' : rec.no_of_parcels,
                'contact_person' : transporter.contact_person,
                'route_id' : rec.transporter_route.id
                }
            # Create a new transport entry
            entry_rec = self.env['transport.entry'].create(transport_entry_vals)

            # Fetch transport location details based on the new transport entry and populate tracking number
            # if entry_rec:
            #     # Update the transport location details with the tracking number
            #     for location in entry_rec.location_route_ids:
            #         location.tracking_num = self.tracking_num



            # Search for the related picking record using delivery_order_id
            picking = self.env['transport.entry'].search([('delivery_order_id', '=', rec.id)], limit=1)

            if picking:

                rec.transport_entry_ids = [(4,entry_rec.id)] # link to the existing record with id=ID(add a relationship)

        return res















