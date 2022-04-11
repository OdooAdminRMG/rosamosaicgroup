# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
	_inherit = "product.template"

	check_relieve_full_lot = fields.Boolean("Relieve Full Lot Quantity from Inventory")

