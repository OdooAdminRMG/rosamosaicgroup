# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockPickingType(models.Model):
	_inherit = "stock.picking.type"

	check_relieve_full_lot = fields.Boolean("Check for Full Lot Quantities During Reservation")

