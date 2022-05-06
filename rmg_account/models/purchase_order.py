# -*- coding: utf-8 -*-

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_account_move_line(self, move=False):
        # Update account_id when BIll genrated from PO
        res = super()._prepare_account_move_line(move)
        if self.product_id.categ_id.property_valuation == 'real_time' and self.product_id.categ_id.property_stock_account_input_categ_id:
            res.update({'account_id': self.product_id.categ_id.property_stock_account_input_categ_id.id})
        return res
