from odoo import _, api, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def create(self, vals):
        """
            Pass 'quant_id' and 'lot_id' while creating the records other fields are related
            so, no need to worry about write operations.
        """
        rtn = super(StockQuant, self).create(vals)
        rtn.lot_id.quant_location_ids.create({'lot_id': rtn.lot_id.id, 'quant_id': rtn.id})
        return rtn

    def create_records_for_existing_data(self):
        """
            Run this scheduled action manually only one time
            to create records for those records
            which are created before the installation of this module.
        """
        self.env['quant.location'].search([]).unlink()
        self.env['stock.quant'].search([]).mapped(
            lambda sq: {sq.lot_id.quant_location_ids.create(
                {
                    'lot_id': sq.lot_id.id,
                    'quant_id': sq.id
                })
            })
