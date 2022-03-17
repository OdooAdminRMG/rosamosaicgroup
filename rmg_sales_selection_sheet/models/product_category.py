# -*- coding: utf-8 -*-
from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "product.category"

    bella_product_categories = fields.Many2one(
        "res.config.settings", string=_("Bella Product Categories")
    )
