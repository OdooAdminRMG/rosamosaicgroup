# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    inv_adj_account_id = fields.Many2one('account.account', string="Inventory Adjustment Account")
