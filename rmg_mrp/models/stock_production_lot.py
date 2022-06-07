from odoo import _, fields, models


class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    quant_location_ids = fields.One2many('quant.location', 'lot_id', string=_("Quants Location Ids"),
                                         readonly=True)
