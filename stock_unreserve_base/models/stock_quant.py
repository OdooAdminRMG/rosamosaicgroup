from odoo import _, api, models
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None,
                                  strict=False):
        # Override this method to prevent 'It is not possible to unreserve more products' error.

        """ Increase the reserved quantity, i.e. increase `reserved_quantity` for the set of quants
        sharing the combination of `product_id, location_id` if `strict` is set to False or sharing
        the *exact same characteristics* otherwise. Typically, this method is called when reserving
        a move or updating a reserved move line. When reserving a chained move, the strict flag
        should be enabled (to reserve exactly what was brought). When the move is MTS,it could take
        anything from the stock, so we disable the flag. When editing a move line, we naturally
        enable the flag, to reflect the reservation according to the edition.

        :return: a list of tuples (quant, quantity_reserved) showing on which quant the reservation
            was done and how much the system was able to reserve on it
        """
        self = self.sudo()
        rounding = product_id.uom_id.rounding
        quants = self._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id,
                              strict=strict)
        reserved_quants = []

        if float_compare(quantity, 0, precision_rounding=rounding) > 0:
            # if we want to reserve
            available_quantity = sum(
                quants.filtered(lambda q: float_compare(q.quantity, 0, precision_rounding=rounding) > 0).mapped(
                    'quantity')) - sum(quants.mapped('reserved_quantity'))
            if float_compare(quantity, available_quantity, precision_rounding=rounding) > 0:
                raise UserError(_('It is not possible to reserve more products of %s than you have in stock.',
                                  product_id.display_name))
        elif float_compare(quantity, 0, precision_rounding=rounding) < 0:
            # if we want to unreserve
            available_quantity = sum(quants.mapped('reserved_quantity'))
            if float_compare(abs(quantity), available_quantity, precision_rounding=rounding) > 0:
                # raise UserError(_('It is not possible to unreserve more products of %s than you have in stock.',
                #                   product_id.display_name))
                return self._update_reserved_quantity(
                    product_id, location_id, -available_quantity, lot_id=lot_id,
                    package_id=package_id, owner_id=owner_id, strict=strict
                )
        else:
            return reserved_quants

        for quant in quants:
            if float_compare(quantity, 0, precision_rounding=rounding) > 0:
                max_quantity_on_quant = quant.quantity - quant.reserved_quantity
                if float_compare(max_quantity_on_quant, 0, precision_rounding=rounding) <= 0:
                    continue
                max_quantity_on_quant = min(max_quantity_on_quant, quantity)
                quant.reserved_quantity += max_quantity_on_quant
                reserved_quants.append((quant, max_quantity_on_quant))
                quantity -= max_quantity_on_quant
                available_quantity -= max_quantity_on_quant
            else:
                max_quantity_on_quant = min(quant.reserved_quantity, abs(quantity))
                quant.reserved_quantity -= max_quantity_on_quant
                reserved_quants.append((quant, -max_quantity_on_quant))
                quantity += max_quantity_on_quant
                available_quantity += max_quantity_on_quant

            if float_is_zero(quantity, precision_rounding=rounding) or float_is_zero(available_quantity,
                                                                                     precision_rounding=rounding):
                break
        return reserved_quants

        return

    # def unlink(self):
    #     if 'is_from_picking_form' in self._context:
    #         precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #         for ml in self:
    #             # Unlinking a move line should unreserve.
    #             if ml.product_id.type == 'product' and ml.move_id and not ml.move_id._should_bypass_reservation(
    #                     ml.location_id) and not float_is_zero(ml.product_qty, precision_digits=precision):
    #                 quants = self.env['stock.quant']._gather(
    #                     ml.product_id, ml.location_id, lot_id=ml.lot_id,
    #                     package_id=ml.package_id, owner_id=ml.owner_id
    #                 )
    #                 available_quantity = sum(quants.mapped('reserved_quantity'))
    #                 qty = available_quantity if available_quantity < ml.product_qty else ml.product_qty
    #                 self.env['stock.quant']._update_reserved_quantity(
    #                     ml.product_id, ml.location_id, -qty,
    #                     lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id, strict=True
    #                 )
    #         moves = self.mapped('move_id')
    #         res = super(models.Model, self).unlink()
    #         if moves:
    #             # Add with_prefetch() to set the _prefecht_ids = _ids
    #             # because _prefecht_ids generator look lazily on the cache of move_id
    #             # which is clear by the unlink of move line
    #             moves.with_prefetch()._recompute_state()
    #         return res
    #     else:
    #         return super(StockMoveLine, self).unlink()
