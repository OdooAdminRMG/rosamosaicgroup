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
        project_task_mo = self.tasks_ids.filtered(
            lambda p: p.peg_to_manufacturing_order
        )
        project_task_do = self.tasks_ids.filtered(
            lambda p: p.peg_to_delivery_order
        )
        move_ids = self.env['procurement.group'].search([
            ('sale_id', 'in', self.ids)
        ]).stock_move_ids
        move_ids.created_production_id.project_task_id = project_task_mo.id
        move_ids.picking_id.project_task_id = project_task_do.id
        return res
