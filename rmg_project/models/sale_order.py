# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import models


class SaleOrder(models.Model):
    """

    """
    _inherit = "sale.order"

    def action_calendar_installation_view(self):
        """

        :return:
        """
        context = self._context.copy()
        context.update({"default_model_id": "sale.order"})
        action_data = self.env.ref(
            "rmg_project.action_calendar_event_project_installation"
        ).read()[0]
        action_data['context'] = context
        return action_data
