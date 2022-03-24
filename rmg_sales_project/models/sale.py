# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import models


class SaleOrder(models.Model):
    """

    """
    _inherit = 'sale.order'

    # create MO record from project.task
    def action_confirm(self):
        """

        """
        res = super(SaleOrder, self).action_confirm()
        project_task = self.tasks_ids.filtered(
            lambda p: p.peg_to_manufacturing_order
        )
        if project_task:
            production_ids = self.env['procurement.group'].search([
                ('sale_id', 'in', self.ids)
            ]).stock_move_ids.created_production_id.ids
            project_task.update({
                'production_ids': [(6, 0, production_ids)]
            })
        return res
