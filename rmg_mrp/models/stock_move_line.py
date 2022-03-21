# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMoveLine(models.Model):
	_inherit = "stock.move.line"

	def assign_all_reserve_qty_lot(self, product_id, picking_type_id, lot_id):
		product_id = self.env['product.product'].browse(product_id)
		picking_type_id = self.env['stock.picking.type'].browse(picking_type_id)
		lot_id = self.env['stock.production.lot'].browse(lot_id)
		if product_id.tracking == 'lot' and product_id.check_relieve_full_lot and picking_type_id.check_relieve_full_lot:
			return lot_id.product_qty
		return False

	@api.model
	def create(self, vals):
		qty = self.assign_all_reserve_qty_lot(vals['product_id'], 2, vals['lot_id']) or 0
		quant = self.env['stock.quant']
		if qty:
			vals['product_uom_qty'] = qty
		res = super(StockMoveLine, self).create(vals)
		if qty:
			quants = self.env['stock.quant']._gather(res.product_id, res.location_id, lot_id=res.lot_id, package_id=res.package_id, owner_id=res.owner_id, strict=False)
			quants.write({'reserved_quantity': qty})
		return res
