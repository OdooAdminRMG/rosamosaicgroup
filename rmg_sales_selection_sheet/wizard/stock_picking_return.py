# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.tools.float_utils import float_round


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    @api.model
    def _prepare_stock_return_picking_line_vals_from_move(self, stock_move):
        res = super(ReturnPicking, self)._prepare_stock_return_picking_line_vals_from_move(stock_move)
        if self._context.get('manually_from_so', False):
            res.update({'quantity': stock_move.product_qty})
        return res
