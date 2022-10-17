from odoo import _, api, models
from odoo.tools import float_is_zero


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def unlink(self):
        if 'is_from_picking_form' in self._context:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            for ml in self:
                # Unlinking a move line should unreserve.
                if ml.product_id.type == 'product' and ml.move_id and not ml.move_id._should_bypass_reservation(
                        ml.location_id) and not float_is_zero(ml.product_qty, precision_digits=precision):
                    quants = self.env['stock.quant']._gather(
                        ml.product_id, ml.location_id, lot_id=ml.lot_id,
                        package_id=ml.package_id, owner_id=ml.owner_id
                    )
                    available_quantity = sum(quants.mapped('reserved_quantity'))
                    qty = available_quantity if available_quantity < ml.product_qty else ml.product_qty
                    self.env['stock.quant']._update_reserved_quantity(
                        ml.product_id, ml.location_id, -qty,
                        lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id, strict=True
                    )
            moves = self.mapped('move_id')
            res = super(models.Model, self).unlink()
            if moves:
                # Add with_prefetch() to set the _prefecht_ids = _ids
                # because _prefecht_ids generator look lazily on the cache of move_id
                # which is clear by the unlink of move line
                moves.with_prefetch()._recompute_state()
            return res
        else:
            return super(StockMoveLine, self).unlink()
