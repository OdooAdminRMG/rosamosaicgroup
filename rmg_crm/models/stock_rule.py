from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _run_buy(self, procurements):
        """
        This method is triggered when any MO try to create or edit PO.
        When the PO is created or updated will pass
        Origin, Product and Product QTY ot create Replenish Source History.
        """
        super(StockRule, self)._run_buy(procurements)
        for procurement, rule in procurements:
            if not self.env["sale.order"].search([("name", "=", procurement.origin)]):
                self.env["purchase.order"].search(
                    [
                        ("origin", "ilike", procurement.origin),
                        ("state", "in", ["draft", "sent"]),
                    ]
                ).filtered(
                    lambda po: procurement.product_id.id
                    in po.order_line.mapped("product_id.id")
                    and procurement.origin
                    not in po.replenish_source_ids.mapped("mo_origin")
                ).write(
                    {
                        "replenish_source_ids": [
                            (
                                0,
                                0,
                                {
                                    "mo_origin": procurement.origin,
                                    "product_id": procurement.product_id.id,
                                    "product_uom_qty": procurement.product_qty,
                                },
                            )
                        ]
                    }
                )
