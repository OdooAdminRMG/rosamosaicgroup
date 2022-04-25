# -*- coding: utf-8 -*-
import logging
from ast import literal_eval

from lxml import etree
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class RmgSale(models.Model):
    _name = "rmg.sale"
    _description = "rmg sale"
    _rec_name = "order_line_id"

    order_id = fields.Many2one("sale.order")
    order_line_id = fields.Many2one("sale.order.line")
    mrp_order_id = fields.Many2one("mrp.production", string="MRP Order Id")
    # order_line_ids = fields.One2many("sale.order.line", 'rmg_sale_id', string=_("Order Lines"))
    order_line_ids = fields.Many2many(
        "sale.order.line", compute="compute_order_lines", string="Order Lines"
    )
    # Do not allow creation of new values.
    corner_treatments_id = fields.Many2one(
        "corner.treatments", string=_("Corner Treatments")
    )
    customer_sink_types_id = fields.Many2one(
        "customer.sink.types", string=_("Customer Sink Types")
    )
    # Do not allow creation of new values.
    edge_profiles_id = fields.Many2one("edge.profiles", string=_("Edge Profiles"))
    faucets_id = fields.Many2one("faucets", string=_("Faucets"))
    # Do not allow creation of new values.
    range_types_id = fields.Many2one("range.types", string=_("Range Types"))
    # Pass this value to the transfer from the warehouse to pre - production.
    slab_tagged_id = fields.Many2one("stock.production.lot", string=_("Slab Tagged"))
    slab_notes = fields.Text(string=_("Slab Notes"))

    def _get_sink_by_bella_domain(self):
        res = self.env["ir.config_parameter"].sudo().get_param(
            "rmg_sales_selection_sheet.sink_by_bella_product_categories"
        )
        res = literal_eval(res) if res else []
        childs = self.rec_child(res)

        return [("categ_id", "in", childs)]

    # Do not allow creation of new values.Only allow products whose Product Category is tiered into(i.e.child of) one
    # or more of threading product categories maintained in Sales > Configuration > Sink By Bella Product Categories
    sink_by_bella_id = fields.Many2one(
        "product.product", string=_("Sink by Bella"), domain=_get_sink_by_bella_domain
    )
    # Only make this field visible if the Customer Sink value is populated.
    customer_sink_model_number = fields.Text(string=_("Customer Sink Model Number"))
    # Only make this field visible if the Faucet value is populated.
    faucet_model = fields.Text(string=_("Faucet Model"))
    additional_holes = fields.Text(string=_("Additional Holes"))
    # Only make this field visible if the Range Type value is populated.
    range_model = fields.Text(string=_("Range Model"))
    # Only make this field visible if the Corner Treatment value is populated.
    corner_treatment_notes = fields.Text(string=_("Corner Treatment Notes"))
    shop_notes = fields.Text(string=_("Shop Notes"))
    installation_notes = fields.Text(string=_("Installation Notes"))
    splash = fields.Text(string=_("Splash"))
    installed_square_footage = fields.Float(string=_("Installed Square Footage"))
    # Used to store the expected square footage used of the slab which will be consumed by the Manufacturing Order
    # Update Component quantity on MO, also transfer this value to the Selection
    # Sheet tab on the MO.Also, propagate this value to any PO generated by the MO
    square_footage_estimate = fields.Float(string=_("Square Footage Estimate"))
    old_square_footage_estimate = fields.Float(
        string=_("Duplicate Square Footage Estimate"), invisible=True
    )

    # Only show records whose department_id value is one of those maintained in Sales > Configuration > Selection Sheet > Template Departments
    def _get_template_by_id_domain(self):
        res = self.env["ir.config_parameter"].sudo().get_param(
            "rmg_sales_selection_sheet.template_departments"
        )
        res = literal_eval(res) if res else []

        return [("department_id", "in", res)]

    templated_by_id = fields.Many2one(
        "hr.employee", string=_("Templated by"), domain=_get_template_by_id_domain
    )
    status = fields.Selection(
        [("new", "New"), ("pre_release", "Pre-Release"), ("released", "Released")],
        string=_("Status"),
        default="new",
    )

    @api.model
    def create(self, vals):
        if vals:
            vals["status"] = "pre_release"
        return super().create(vals)

    def rec_child(self, ele):
        temp = ele
        ele = self.env["product.category"].browse(ele)
        for child in ele:
            if child.child_id:
                for i in child.child_id.ids:
                    if i not in temp:
                        temp.append(i)
        if len(temp) != len(ele):
            return self.rec_child(temp)
        else:
            return ele.ids

    @api.depends("order_line_id")
    def compute_order_lines(self):
        self.order_line_ids = self.order_id.order_line.filtered(
            lambda x: x.section_id.id == self.order_line_id.id
        ).mapped("id")

    def open_warning_wizard(self, message):
        """
        It will prepare message and return wizard
        """
        context = dict(self._context)
        context.update({"default_rng_id": self.id, "default_message": message})
        return {
            "type": "ir.actions.act_window",
            "res_model": "rmg.sale.warning.wiz",
            "name": "WARNING",
            "target": "new",
            "views": [(False, "form")],
            "view_mode": "form",
            "view_id": self.env.ref(
                "rmg_sales_selection_sheet.view_rmg_sale_warning_wiz_form"
            ).id,
            "context": context,
        }

    def save_data(self):
        """
        - 'old_square_footage_estimate' field will contain old value of 'square_footage_estimate',
        so that we can check if any changes occur in 'square_footage_estimate' field.
        - Based on condition this method will pop up warning wizards.
        - 'continue' button will again call this method
        but will skip previous po or mo ids and again raise warning based on conditions.
        """
        if not self:
            self = self.env["rmg.sale"].browse(self.env.context.get("rmg_id", False))
        if (
            self.old_square_footage_estimate != self.square_footage_estimate
            or "skip_mo_ids" in self.env.context
            or "skip_po_ids" in self.env.context
        ):
            if self.old_square_footage_estimate != self.square_footage_estimate:
                self.old_square_footage_estimate = self.square_footage_estimate
            mrp = self.env["mrp.production"].search([("rmg_id", "=", self.id)], limit=1)
            if mrp and self.order_id.state == "sale":
                if mrp.state not in ["cancel", "done"]:
                    mrp.move_raw_ids[0].product_uom_qty = self.square_footage_estimate
                    po_ids = (
                        mrp.procurement_group_id.stock_move_ids.created_purchase_line_id.order_id
                        | mrp.procurement_group_id.stock_move_ids.move_orig_ids.purchase_line_id.order_id
                    )
                    for po in po_ids.filtered(
                        lambda po: po.state in ["draft", "purchase"]
                    ):
                        order = po.order_line[0]
                        if po.state == "draft":
                            order.product_qty = self.square_footage_estimate
                        elif po.state == "purchase":
                            skip_po_ids = self.env.context.get("skip_po_ids", [])
                            if po.id not in skip_po_ids:
                                skip_po_ids.append(po.id)
                                return self.with_context(
                                    {"rmg_id": self.id, "skip_po_ids": skip_po_ids}
                                ).open_warning_wizard(
                                    "A Purchase Order has already been created for the component material {} in the quantity of {}. Since you have updated the Estimated Square Footage, you will need to manually update that Purchase Order. Do you wish to proceed?".format(
                                        order.product_id.name, order.product_qty
                                    )
                                )
                else:
                    skip_mo_ids = self.env.context.get("skip_mo_ids", [])
                    if mrp.id not in skip_mo_ids:
                        skip_mo_ids.append(mrp.id)
                        return self.with_context(
                            {"rmg_id": self.id, "skip_mo_ids": skip_mo_ids}
                        ).open_warning_wizard(
                            "The Manufacturing Order generated for this Sales Order Line has already been canceled or marked as done.The change to the Estimated Square Footage value will not be passed to any manufacturing order and you will need to manually incorporate these changes."
                        )

        if (
            self.order_id.state == "sale"
            and self.status == "pre_release"
            and self.square_footage_estimate >= 0
        ):
            self.status = "released"
        return
