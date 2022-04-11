# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models


class StockPicking(models.Model):
    """

    """
    _inherit = "stock.picking"

    project_task_id = fields.Many2one('project.task', string="Project Task")

    def action_link_do_with_task(self):
        """

        """
        picking_ids = self.browse(self._context.get('active_ids'))
        if self._context.get('task_id', False):
            task_id = self.env['project.task'].browse(self._context.get('task_id', False))
            picking_ids.project_task_id = self._context.get('task_id', False)
            picking_ids.scheduled_date = task_id.planned_date_end
            picking_ids.date_deadline = task_id.planned_date_end
