from odoo import _, api, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def create(self, vals):
        rtn = super(StockQuant, self).create(vals)
        rtn.lot_id.quant_location_ids.create({'lot_id': rtn.lot_id.id, 'quant_id': rtn.id})
        return rtn
