# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    temp_user_ids = fields.Many2many('res.users', string="Templator", compute='_get_user')
    project_manager_id = fields.Many2one('res.users', string="Project Manager", compute='_get_user')

    def _get_user(self):
        self.temp_user_ids = False
        self.project_manager_id = False
        for MO in self:
            task_ids = self.env['project.task'].search([
                ('job_name', '=', self.job_name), ('is_template_task', '=', True)])
            if task_ids:
                for task in task_ids:
                    MO.write({
                            'temp_user_ids': [(4, user.id) for user in task.user_ids],
                        })
            project_id = self.env['project.project'].search([
                ('job_name', '=', self.job_name)], limit=1)
            if project_id:
                MO.write({
                        'project_manager_id': project_id.user_id.id,
                    })


