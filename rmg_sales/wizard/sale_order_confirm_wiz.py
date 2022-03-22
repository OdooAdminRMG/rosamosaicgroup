# -*- coding: utf-8 -*-

from odoo import api, models, fields

class SaleOrderConfirmWiz(models.TransientModel):
    _name = "sale.order.confirm.wiz"

    sale_id = fields.Many2one('sale.order')
    message = fields.Html(string="Message", default="")

    def confirm_so(self):
        print ("self>> context>>>", self._context)
        copy_context = dict(self.env.context)
        copy_context.pop('from_so_action_confirm', None)
        if self.sale_id:
            return self.sale_id.with_context(copy_context).action_confirm()
