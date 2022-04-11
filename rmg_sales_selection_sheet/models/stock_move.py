# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move"

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        """
        This method will pass slab_tagged_id to delivery order If MO is created and internal transfer is triggered.
        Return: Dictionary of values with lot_id
        bom_line_id: Fetch record of bom product for product in sale order_line
        """
        rtn = super(StockMoveLine, self)._prepare_move_line_vals(
            quantity, reserved_quant
        )

        for line in self.picking_id.sale_id.order_line.filtered(
            lambda line: line.display_type == False and line.rmg_sale_id and line.rmg_sale_id.slab_tagged_id
        ):
            bom_line_ids = (
                self.env["mrp.bom"]
                .search(
                    [
                        "|",
                        "|",
                        ("byproduct_ids.product_id", "=", self.product_id.id),
                        ("product_id", "=", line.product_id.id),
                        "&",
                        ("product_id", "=", False),
                        ("product_tmpl_id", "=", line.product_id.product_tmpl_id.id),
                    ]
                )
                .bom_line_ids
            )
            for bom_line_id in bom_line_ids:
                if bom_line_id and rtn.get("product_id") == bom_line_id.product_id.id:
                    rtn.update({"lot_id": line.rmg_sale_id.slab_tagged_id.id})
        return rtn
