# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
	_inherit = "sale.order"

	def action_confirm(self):
		res = super(SaleOrder, self).action_confirm()
		for move_line in self.picking_ids.move_line_ids.filtered(lambda x : x.product_id.tracking == 'lot'):
			if move_line.lot_id:
				# Reserved entire lot in Picking
				move_line.write({'product_uom_qty': move_line.lot_id.product_qty})
		return res