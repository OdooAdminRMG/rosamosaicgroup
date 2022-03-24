# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    selection_sheet_notes = fields.Text(string=_("Notes"))
    transferred_to_mo = fields.Boolean('Transferred to MO')

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
        # self.env['rmg.sale'].compute_order_lines(self)
        return

    def action_confirm(self):
        rmg_order_line = []
        for rec in self.order_line:
            if rec.display_type == "line_section":
                lst = self.order_line.filtered(lambda x: x.section_id == rec
                                  and self.env.ref('stock.route_warehouse0_mto') in x.product_id.route_ids
                                  and self.env.ref('mrp.route_warehouse0_manufacture') in x.product_id.route_ids)
                if len(l) == 0:

                    raise UserError(_("In %s section have at least one product with MTO option in route") % (rec.name))
                if len(lst) > 1:
                    raise UserError(_("More than one product in the section %s has both its Replenish to Order (MTO) "
                                      "and Manufacture routes selected. Confirming or Saving this change would result in"
                                      " multiple Manufacturing Orders being created. Since there is only one set of "
                                      "Selection Sheet data per Sales Order section, the system cannot identify which "
                                      "Manufacturing Order is relevant for the Selection Sheet data. Please specify only "
                                      "a single Sales Order Line whose product has these two routes set on its product template.") % (rec.name))
                rmg_order_line.append(lst.mapped('rmg_sale_id'))
        res = super(SaleOrder, self).action_confirm()
        if rmg_order_line:
            for rec in rmg_order_line:
                rec.update({'status' : 'released'})
        return res

    def action_draft(self):
        res = super(SaleOrder, self).action_draft()
        rmg_sales = self.order_line.mapped('rmg_sale_id')
        if rmg_sales:
            rmg_sales.update({'status' : 'pre_release'})
        return res

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    rmg_sale_id = fields.Many2one(
        "rmg.sale",
        compute='compute_rmg_sale_id',
        string="RMG Sale Id")
    section_id = fields.Many2one("sale.order.line", string="Section Id", store=True)
    mrp_order_id = fields.Many2one("mrp.production", string="MRP Order Id")

    def compute_rmg_sale_id(self):
        for rec in self:
            lines = rec.env["rmg.sale"].search(
                [("order_line_id", "=", rec.section_id.id)]
            )
            rec.rmg_sale_id = lines.id if lines else False
