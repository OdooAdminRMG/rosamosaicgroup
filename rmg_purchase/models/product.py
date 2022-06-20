from odoo import fields, models


class Product(models.Model):
    _inherit = "product.product"

    def _name_search(
            self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        """
        If this method is called from move_line_nosuggest_ids of stock.picking
        then based on selected products of move_ids_without_package it will create a domain.
        """
        if args is None:
            args = []
        if (
                "stock_picking_id" in self._context
                and "stock_picking_type" in self._context
        ):
            picking_type_id = self.env["stock.picking.type"].browse(
                self.env.context.get("stock_picking_type")
            )
            if picking_type_id and picking_type_id.code == "incoming":
                product_ids = (
                    self.env["stock.picking"]
                    .browse(self.env.context.get("stock_picking_id"))
                    .move_ids_without_package.mapped("product_id")
                )
                if product_ids: args += [("id", "in", product_ids.ids)]
        return super(Product, self)._name_search(
            name, args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )
