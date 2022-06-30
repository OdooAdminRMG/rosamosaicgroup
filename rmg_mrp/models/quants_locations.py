from odoo import _, fields, models


class QuantLocations(models.Model):
    _name = 'quant.location'
    _description = "Create records for each location of respective lot." \
                   "" \
                   "Important: Please runt scheduled action named " \
                   "'create_records_for_existing_data' manually (Only One Time)" \
                   "which will create records for those records " \
                   "which are created before the installation of this module." \
                   "" \
                   "Note: Pass 'quant_id' and 'lot_id' while creating the records other fields are related " \
                   "so, no need to worry about write operations"
    _rec_name = "name"

    lot_id = fields.Many2one('stock.production.lot', string=_('Lot/Serial Number'), domain=[('id', '=', False)],
                             required=True)
    quant_id = fields.Many2one('stock.quant', string=_('Quant'))

    name = fields.Char(string=_('Lot/Serial Number'), related="lot_id.name")
    ref = fields.Char(string=_('Internal Reference'), related="lot_id.ref")
    product_id = fields.Many2one(related="lot_id.product_id")
    product_qty = fields.Float(string=_('Quantity'), related="lot_id.product_qty")
    company_id = fields.Many2one('Company', related="lot_id.company_id")

    location_id = fields.Many2one(related="quant_id.location_id", string=_("Location"))
    inventory_quantity_auto_apply = fields.Float(related="quant_id.inventory_quantity_auto_apply",
                                                 string=_("Quantity On Hand"), store=True)
