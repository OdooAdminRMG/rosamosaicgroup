# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderConfirmWiz(models.TransientModel):
    _name = "sale.order.confirm.wiz"

    sale_id = fields.Many2one("sale.order")
    message = fields.Html(string="Message", default="")

    def confirm_so(self):
        copy_context = dict(self.env.context)
        if self.sale_id:
            return self.sale_id.with_context(copy_context).action_confirm()
