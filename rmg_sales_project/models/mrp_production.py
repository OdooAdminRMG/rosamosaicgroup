# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    project_task_id = fields.Many2one('project.task', string="Tasks")

    def action_link_mo_with_task(self):
        """

        """
        mrp_active_id = self.browse(self._context.get('active_ids'))
        if self._context.get('task_id', False):
            task_id = self.env['project.task'].browse(self._context.get('task_id', False))
            mrp_active_id.project_task_id = task_id
            mrp_active_id.date_planned_start = task_id.planned_date_end
