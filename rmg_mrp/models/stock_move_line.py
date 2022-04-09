# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockMove(models.Model):
	_inherit = "stock.move"

	def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
		res = super(StockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
		# Pass Picking Type in move line vals
		res.update({'picking_type_id': self.picking_type_id and self.picking_type_id.id or False})
		return res

class StockMoveLine(models.Model):
	_inherit = "stock.move.line"

	def assign_all_reserve_qty_lot(self, product_id, picking_type_id, lot_id):
		product_id = self.env['product.product'].browse(product_id)
		picking_type_id = self.env['stock.picking.type'].browse(picking_type_id)
		lot_id = self.env['stock.production.lot'].browse(lot_id)
		# Check if Product is traced by Lot and Picking Type and Product have check_relieve_full_lot flag checked
		if product_id.tracking == 'lot' and product_id.check_relieve_full_lot and picking_type_id.check_relieve_full_lot:
			# If condition matched then return Lot's Qty
			return lot_id.product_qty
		return False

	@api.model
	def create(self, vals):
		picking_type_id = vals.get('picking_type_id', False)
		product_id = vals.get('product_id', False)
		lot_id = vals.get('lot_id', False)
		updated_qty = False
		# Pass Product, Picking Type and Lot
		if product_id and picking_type_id and lot_id:
			updated_qty = self.assign_all_reserve_qty_lot(product_id, picking_type_id, lot_id)
			if updated_qty:
				# Update Move line Reserved qty with Lot's qty
				vals['product_uom_qty'] = updated_qty
		res = super(StockMoveLine, self).create(vals)
		if updated_qty:
			# Update Quant reserved qty as per Stock Move line's Reserved QTY. It helps us in Forecast qty report
			quants = self.env['stock.quant']._gather(res.product_id, res.location_id, lot_id=res.lot_id, package_id=res.package_id, owner_id=res.owner_id, strict=False)
			quants.write({'reserved_quantity': updated_qty})
		return res


