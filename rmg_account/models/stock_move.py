# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_src_account(self, accounts_data):
        """
            Overide Method to get custom account when created Journal entries

        """
        if self.product_id.categ_id.property_valuation == 'real_time' and self.product_id.categ_id.inv_adj_account_id and self.origin:
            return self.location_id.valuation_out_account_id.id or accounts_data['stock_input'].id
        else:
            return self.location_dest_id.valuation_in_account_id.id or self.product_id.categ_id.inv_adj_account_id.id

    def _get_dest_account(self, accounts_data):
        """
            Overide Method to get custom account when created Journal entries

        """
        if self.product_id.categ_id.property_valuation == 'real_time' and self.product_id.categ_id.inv_adj_account_id and self.origin:
            return self.location_dest_id.valuation_in_account_id.id or accounts_data['stock_output'].id
        else:
            return self.location_dest_id.valuation_in_account_id.id or self.product_id.categ_id.inv_adj_account_id.id
