# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockPickingType(models.Model):
	_inherit = "stock.picking.type"

	check_relieve_full_lot = fields.Boolean("Check for Full Lot Quantities During Reservation")

class StockPicking(models.Model):
	_inherit = "stock.picking"

	def action_assign(self):
		res = super(StockPicking, self).action_assign()
		for move_line in self.move_ids_without_package.filtered(lambda x: x.product_id.tracking == 'lot').move_line_ids:
			if move_line.lot_id and move_line.product_id.check_relieve_full_lot and move_line.picking_id and move_line.picking_id.picking_type_id.check_relieve_full_lot:
				# Reserved entire lot in Picing
				move_line.write({'product_uom_qty': move_line.lot_id.product_qty})
		return res
