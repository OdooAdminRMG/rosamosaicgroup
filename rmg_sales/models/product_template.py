# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_hide_from_sale_report = fields.Boolean(string="Hide From Sale Order Report")
