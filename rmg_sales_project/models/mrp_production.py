# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import _, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    installation_date = fields.Datetime(string=_("Installation Date"), compute="_compute_installation_date")
    project_task_id = fields.Many2one('project.task', string=_("Tasks"))

    def _compute_installation_date(self):
        for production in self:
            production.installation_date = False
            sale_order_ids = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id
            if sale_order_ids:
                delivery_task_ids = sale_order_ids.tasks_ids.filtered('peg_to_delivery_order')
                if delivery_task_ids:
                    production.installation_date = delivery_task_ids[0].planned_date_begin

    def action_link_mo_with_task(self):
        """

        """
        mrp_active_id = self.browse(self._context.get('active_ids'))
        if self._context.get('task_id', False):
            task_id = self.env['project.task'].browse(self._context.get('task_id', False))
            mrp_active_id.project_task_id = task_id
            mrp_active_id.date_planned_start = task_id.planned_date_end
            mrp_active_id.date_deadline = task_id.planned_date_end
