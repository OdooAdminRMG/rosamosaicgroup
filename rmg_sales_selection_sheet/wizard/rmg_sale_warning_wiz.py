# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class RmgSaleWarningWiz(models.TransientModel):
    _name = "rmg.sale.warning.wiz"

    rmg_id = fields.Many2one("rmg.sale")
    message = fields.Html(string="Message", default="")

    def continue_rmg_sale(self):
        """
        It will call 'save_data' method again.
        """
        copy_context = dict(self.env.context)
        return self.rmg_id.with_context(copy_context).save_data()

    def open_rmg_selection_sheet(self):
        """
        It will redirect user to the current 'RMG Selection Sheet'.
        """
        return {
            "name": _("RMG Selection Sheet"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "res_model": "rmg.sale",
            "target": "new",
            "res_id": self.env.context.get("rmg_id"),
        }
