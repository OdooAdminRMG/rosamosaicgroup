# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    selection_sheet_notes = fields.Text(string=_("Notes"))
    transferred_to_mo = fields.Boolean("Transferred to MO")

    @api.model
    def create(self, value):
        rtn = super(SaleOrder, self).create(value)
        section_id = False
        for so in rtn.order_line:
            if so.display_type == "line_section":
                section_id = so.id
            elif so.display_type != "line_note" and section_id:
                so.update({"section_id": int(section_id)})
            else:
                pass
        return rtn

    @api.onchange("order_line")
    def onchange_order_line(self):
        sections = self.order_line.filtered(lambda x: x.display_type == "line_section")
        sections = sections.sorted(lambda x: x.sequence)
        for rec in self.order_line:
            if not rec.display_type:
                rec.section_id = False
                for seq in sections:
                    if seq.sequence < rec.sequence:
                        rec.section_id = int(seq._origin.id)
        return

    def action_confirm(self):
        rmg_order_line = []
        flag = []
        # Check Selection Sheet
        selection_sheet_enable = self.env['ir.config_parameter'].sudo().get_param('rmg_sales_selection_sheet.companies')
        if selection_sheet_enable:
            not_selection_sheet_lines = self.order_line.filtered(
                lambda x: x.display_type != "line_section" and not x.rmg_sale_id and x.section_id)
            if not_selection_sheet_lines:
                raise UserError(
                    _("Please add Selection sheet to the Section : %s") % (','.join(not_selection_sheet_lines.mapped('section_id').mapped('name'))))
        # Check Square Footage Estimation
        footage_lst = self.order_line.filtered(
            lambda x: x.display_type != "line_section" and x.rmg_sale_id and x.rmg_sale_id.square_footage_estimate <= 0)
        if footage_lst:
            raise UserError(
                _("Please add square footage estimate value in Section : %s ") % (','.join(footage_lst.mapped('section_id').mapped('name'))))
        for rec in self.order_line:
            if rec.display_type == "line_section":
                lst = self.order_line.filtered(lambda x: x.section_id == rec
                                                         and self.env.ref(
                    'stock.route_warehouse0_mto') in x.product_id.route_ids
                                                         and self.env.ref(
                    'mrp.route_warehouse0_manufacture') in x.product_id.route_ids
                                                         and x.rmg_sale_id.status != 'released')
                if len(lst) > 1:
                    raise UserError(
                        _(
                            "More than one product in the section %s has both its Replenish to Order (MTO) "
                            "and Manufacture routes selected. Confirming or Saving this change would result in"
                            " multiple Manufacturing Orders being created. Since there is only one set of "
                            "Selection Sheet data per Sales Order section, the system cannot identify which "
                            "Manufacturing Order is relevant for the Selection Sheet data. Please specify only "
                            "a single Sales Order Line whose product has these two routes set on its product template."
                        )
                        % (rec.name)
                    )
                rmg_order_line.append(lst.mapped("rmg_sale_id"))
            if (
                    rec.product_id and self.env.ref("stock.route_warehouse0_mto")
                    in rec.product_id.route_ids
                    and self.env.ref("mrp.route_warehouse0_manufacture")
                    in rec.product_id.route_ids
                    and not self.env["mrp.bom"]
                    .search(
                [
                    "|",
                    "|",
                    ("byproduct_ids.product_id", "=", rec.product_id.id),
                    ("product_id", "=", rec.product_id.id),
                    "&",
                    ("product_id", "=", False),
                    ("product_tmpl_id", "=", rec.product_id.product_tmpl_id.id),
                ]
            )
                    .bom_line_ids.ids
            ):
                flag.append(rec.product_id.name)
        if flag:
            flag = ", ".join(flag)
            raise UserError(
                _(
                    "Please define BOM in: %s"
                )
                % (flag)
            )

        res = super(SaleOrder, self).action_confirm()
        if rmg_order_line and self.state in ["sale"]:
            for rec in rmg_order_line:
                rec.update({"status": "released"})
        return res

    def action_draft(self):
        res = super(SaleOrder, self).action_draft()
        rmg_sales = self.order_line.mapped("rmg_sale_id")
        if rmg_sales:
            rmg_sales.update({"status": "pre_release"})
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    rmg_sale_id = fields.Many2one(
        "rmg.sale", compute="compute_rmg_sale_id", string="RMG Sale Id"
    )
    section_id = fields.Many2one("sale.order.line", string="Section Id", store=True)
    mrp_order_id = fields.Many2one("mrp.production", string="MRP Order Id")

    def compute_rmg_sale_id(self):
        section_id = False
        for rec in self:
            if rec.display_type == "line_section":
                section_id = rec.id
            elif rec.display_type != "line_note" and section_id:
                rec.update({"section_id": int(section_id)})
            else:
                pass
            lines = rec.env["rmg.sale"].search(
                [("order_line_id", "=", rec.section_id.id)]
            )
            rec.rmg_sale_id = lines.id if lines else False

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(SaleOrderLine, self).create(vals_list)
        for line in lines.filtered(lambda line: line.state == 'sale'):
            if line.display_type == 'line_section':
                self.env['rmg.sale'].create({
                    'order_id': line.order_id.id,
                    'order_line_id': line.id,
                    'square_footage_estimate': 0,
                })
        section_id = False
        for so in lines:
            if so.display_type == "line_section":
                section_id = so.id
            elif so.display_type != "line_note" and section_id:
                so.update({"section_id": int(section_id)})
            else:
                pass
        lines.filtered(lambda line: line.state == 'sale')._action_launch_stock_rule()
        procurement_groups = self.env['procurement.group'].search([('sale_id', '=', lines.order_id.id)])
        mrp_production_ids = procurement_groups.stock_move_ids.created_production_id.ids
        for rec in mrp_production_ids:
            mrp_id = self.env['mrp.production'].browse(rec)
            if mrp_id.procurement_group_id.mrp_production_ids.move_dest_ids.sale_line_id.id in lines.filtered(
                    lambda line: line.state == 'sale').ids:
                mrp_id.rmg_id = lines[-1].rmg_sale_id.id if lines else False
                for mrp_line in mrp_id.move_raw_ids:
                    mrp_line.product_uom_qty = mrp_id.rmg_id.square_footage_estimate
        return lines

    def unlink(self):
        # Unlink Rmg Sale ID when deleting line_section order line
        for rec in self:
            if rec.display_type == "line_section" and rec.rmg_sale_id:
                rec.rmg_sale_id.sudo().unlink()
        return super(SaleOrderLine, self).unlink()
