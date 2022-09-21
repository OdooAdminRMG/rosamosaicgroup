# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ReplenishSources(models.Model):
    _name = "replenish.sources"
    _description = "Replenish Sources"

    # The records of this model will be either created from Sale Order or from Manufacturing Order.
    # Only need to pass 'so_line_id' or 'mo_origin' while creating the records
    # The other value will be computed based on it.

    po_id = fields.Many2one(
        "purchase.order",
        string=_("Purchase Order"),
        ondelete="cascade",
    )
    so_line_id = fields.Many2one(
        "sale.order.line",
        string=_("Sale Order Line"),
        ondelete="cascade",
    )
    mo_id = fields.Many2one(
        "mrp.production",
        compute="_compute_mo_id",
        string="Manufacturing Order",
        store=True,
        ondelete="cascade",
    )
    mo_origin = fields.Char(
        string=_("Manufacturing Origin"),
    )

    so_id = fields.Many2one(
        related="so_line_id.order_id",
        string=_("Sale Order"),
        store=True,
    )
    job_name = fields.Char(
        compute="_compute_replenish_sources_data",
        string=_("Job Name"),
        store=True,
        help="1. Carry Job Name from MO if RFQ was created as a result of a product "
        "having its Replenish to Order (MTO) route selected and a parent MO "
        "being created which had a Job Name assigned."
        "2. Carry Job Name from SO if RFQ was created as a result of a product "
        "having its Replenish to Order (MTO) route selected and a parent SO "
        "being created which had a Job Name assigned.",
    )
    product_id = fields.Many2one(
        "product.product",
        compute="_compute_replenish_sources_data",
        string=_("Product"),
        store=True,
    )
    product_uom_qty = fields.Float(
        compute="_compute_replenish_sources_data",
        string=_("Quantity"),
        store=True,
    )
    price_unit = fields.Float(
        compute="_compute_replenish_sources_data",
        string=_("Unit Price"),
        store=True,
    )

    requested_by = fields.Many2one(
        "res.users",
        default=lambda self: self.env.user,
        string=_("Requested By"),
    )
    requested_on = fields.Datetime(
        string=_("Requested On"), default=lambda self: fields.Datetime.now()
    )

    @api.depends(
        "so_id.job_name",
        "so_line_id.product_id",
        "po_id.order_line.price_unit",
        "so_line_id.product_uom_qty",
        "mo_id.job_name",
        "product_id.lst_price",
    )
    def _compute_replenish_sources_data(self):
        """
        If the RFQ is created from Sale Order then we'll have Sale Order Line,
        so we can get other values from it.
        but if the RFQ is created from Manufacturing Order then we'll have Manufacturing Order origin,
        so we can compute other values from it.
        """
        for rec in self:
            if rec.so_line_id:
                rec.job_name = rec.so_id.job_name
                rec.product_id = rec.so_line_id.product_id
                rec.product_uom_qty = rec.so_line_id.product_uom_qty
            else:
                rec.job_name = rec.mo_id.job_name
            rec.price_unit = sum(
                rec.po_id.order_line.filtered(
                    lambda po_line: po_line.product_id.id == rec.product_id.id
                ).mapped("price_unit")
            )

    @api.depends("mo_origin")
    def _compute_mo_id(self):
        for rec in self:
            rec.mo_id = (
                self.env["mrp.production"]
                .search(
                    [
                        ("name", "=", rec.mo_origin),
                    ]
                )
                .id
            )

    def create_replenish_sources_history_for_existing_po(self):
        """
        This scheduled action will create Replenish History
        for the records which are created before the installation of this module.
        """
        self.env["replenish.sources"].search([]).unlink()
        for po in self.env["purchase.order"].search([]):
            for so_rs in (
                self.env["sale.order.line"]
                .search(
                    [
                        ("order_id", "in", po._get_sale_orders().ids),
                        ("product_id", "in", po.order_line.mapped("product_id.id")),
                    ]
                )
                .ids
            ):
                po.write({"replenish_source_ids": [(0, 0, {"so_line_id": so_rs})]})
            for mo_rs in self.env["stock.move"].search(
                [
                    ("raw_material_production_id", "in", po._get_mrp_productions().ids),
                    ("product_id", "in", po.order_line.mapped("product_id.id")),
                ]
            ):
                po.write(
                    {
                        "replenish_source_ids": [
                            (
                                0,
                                0,
                                {
                                    "mo_origin": mo_rs.raw_material_production_id.name,
                                    "product_id": mo_rs.product_id.id,
                                    "product_uom_qty": mo_rs.product_qty,
                                },
                            )
                        ],
                    }
                )
