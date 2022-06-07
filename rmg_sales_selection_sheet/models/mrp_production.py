from ast import literal_eval

from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_order_line_ids = fields.One2many(
        "sale.order.line", "mrp_order_id", string="Sale Order Lines"
    )
    rmg_ids = fields.One2many("rmg.sale", "mrp_order_id", string="Rmg Lines")
    rmg_id = fields.Many2one("rmg.sale", string="Rmg Id")
    edge_profiles_id = fields.Many2one("edge.profiles", string=_("Edge Profiles"), related="rmg_id.edge_profiles_id")
    splash = fields.Text(string=_("Splash"), related="rmg_id.splash")
    slab_tagged_id = fields.Many2one(
        "stock.production.lot", related="rmg_id.slab_tagged_id", string=_("Slab Tagged")
    )
    slab_notes = fields.Text(related="rmg_id.slab_notes", string=_("Slab Notes"))
    sink_by_bella_id = fields.Many2one(
        "product.product", related="rmg_id.sink_by_bella_id", string=_("Sink by Bella")
    )
    customer_sink_types_id = fields.Many2one(
        "customer.sink.types",
        related="rmg_id.customer_sink_types_id",
        string=_("Customer Sink Types"),
    )
    customer_sink_model_number = fields.Text(
        related="rmg_id.customer_sink_model_number",
        string=_("Customer Sink Model Number"),
    )
    shop_notes = fields.Text(related="rmg_id.shop_notes", string=_("Shop Notes"))
    installation_notes = fields.Text(
        related="rmg_id.installation_notes", string=_("Installation Notes")
    )
    square_footage_estimate = fields.Float(
        related="rmg_id.square_footage_estimate", string=_("Square Footage Estimate")
    )
    installed_square_footage = fields.Float(related="rmg_id.square_footage_estimate",
                                            string=_("Installed Square Footage"))
    templated_by_id = fields.Many2one(
        "hr.employee", related="rmg_id.templated_by_id", string=_("Templated by")
    )

    def _get_move_raw_values(
            self,
            product_id,
            product_uom_qty,
            product_uom,
            operation_id=False,
            bom_line=False,
    ):
        data = super()._get_move_raw_values(
            product_id, product_uom_qty, product_uom, operation_id=False, bom_line=False
        )
        data.update(
            {
                "product_uom_qty": self.square_footage_estimate
                if self.rmg_id and self.square_footage_estimate
                else product_uom_qty,
            }
        )
        return data


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_mo_vals(
            self,
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
    ):
        res = super()._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        if values.get("move_dest_ids"):
            # res['rmg_ids'] = [(4, x.sale_line_id.rmg_sale_id.id) for x in values['move_dest_ids']] if values['move_dest_ids'] else False
            res["rmg_id"] = (
                values["move_dest_ids"].sale_line_id.rmg_sale_id.id
                if values["move_dest_ids"]
                else False
            )
        return res
