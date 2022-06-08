from odoo import _, fields, models


class QuantLocations(models.Model):
    _name = 'quant.location'
    _description = "Create records for each location of respective lot."
    _rec_name = "name"

    lot_id = fields.Many2one('stock.production.lot', string=_('Stock Production Lot Id'), invisible=True)
    quant_id = fields.Many2one('stock.quant', string=_('Stock Quant Id'), invisible=True)

    name = fields.Char(string=_('Lot/Serial Number'), related="lot_id.name")
    ref = fields.Char(string=_('Internal Reference'), related="lot_id.ref")
    product_id = fields.Many2one(related="lot_id.product_id")
    product_qty = fields.Float(string=_('Quantity'), related="lot_id.product_qty")
    company_id = fields.Many2one('Company', related="lot_id.company_id")

    location_id = fields.Many2one(related="quant_id.location_id", string=_("Location"))
    inventory_quantity_auto_apply = fields.Float(related="quant_id.inventory_quantity_auto_apply",
                                                   string=_("Quantity On Hand"), store=True)
