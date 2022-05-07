# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_calendar_installation_view(self):
        action_data = self.env.ref(
            "rmg_project.action_calendar_event_project_installation").read()[0]
        action_data.update(
            {

                "context": {
                    "default_model_id": "sale.order",

                },
            }
        )
        return action_data
