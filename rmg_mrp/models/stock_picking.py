# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPicking(models.Model):
	_inherit = "stock.picking"

	def action_assign(self):
		res = super(StockPicking, self).action_assign()
		for move_line in self.move_ids_without_package.filtered(lambda x: x.product_id.tracking == 'lot').move_line_ids:
			if move_line.lot_id:
				# Reserved entire lot in Picking
				move_line.write({'product_uom_qty': move_line.lot_id.product_qty})
		return res
