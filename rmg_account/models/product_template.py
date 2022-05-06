# -*- coding: utf-8 -*-


from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_product_accounts(self):
        """ Add the stock accounts related to product to the result of super()
        @return: dictionary which contains information regarding stock accounts and super (income+expense accounts)
        """
        accounts = super(ProductTemplate, self)._get_product_accounts()
        if self.categ_id.property_valuation == 'real_time' and self.categ_id.inv_adj_account_id:
            accounts.update({
                'stock_input':  self.categ_id.inv_adj_account_id,
                'stock_output': self.categ_id.inv_adj_account_id,
            })
        return accounts
