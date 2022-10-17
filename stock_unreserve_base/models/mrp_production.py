from odoo import _, api, models
from odoo.tools.float_utils import float_compare
from odoo.tools import float_is_zero
from collections import defaultdict
from odoo.tools.misc import OrderedSet, format_date
from odoo.exceptions import UserError


# update stock_quant set reserved_quantity =10  where id= 12;
class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def unlink(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        print("\n\n\n\nself\n\n\n", self._context)
        if 'is_from_picking_form' in self._context:
            print("\n\n\n\nself\n\n\n", self)
            # for ml in self:
            #     Unlinking a move line should unreserve.
    #
    #     return super(StockMoveLine, self).unlink()

    # def _update_reserved_quantity(
    #         self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, strict=False
    # ):
    #     rounding = product_id.uom_id.rounding
    #     quants = self._gather(
    #         product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict
    #     )
    #
    #     if 'is_from_picking_form' in self._context and float_compare(quantity, 0, precision_rounding=rounding) < 0:
    #         # if we want to unreserve
    #         available_quantity = sum(quants.mapped('reserved_quantity'))
    #         print("\n\n\n\n\n--------------------", available_quantity)
    #         if float_compare(abs(quantity), available_quantity, precision_rounding=rounding) > 0:
    #             print("\n\n\n\n\n--------------------", quantity)
    #
    #     return super(StockQuant, self)._update_reserved_quantity(
    #         product_id, location_id, quantity, lot_id, package_id, owner_id, strict
    #     )
