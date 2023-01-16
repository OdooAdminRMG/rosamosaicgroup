
from odoo import models, _


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_edit_stock_quant(self):
        return {
            'name': _('Edit Stock Quant'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'res_model': 'edit.stock.quant.wizard',
            'target': 'new',
            'context': {
                'default_reserved_qty': self.reserved_quantity,
                'default_quant_id': self.id,
            }
        }
