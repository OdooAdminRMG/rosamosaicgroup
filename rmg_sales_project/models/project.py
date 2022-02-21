# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

PROJECT_TASK_READABLE_FIELDS = {'task_id', 'lead_time'}

import logging
_logger = logging.getLogger(__name__)


class project_task(models.Model):
    _inherit = 'project.task'

    task_id = fields.Char(
        string='Task ID',
        default=lambda self: _('New'),
        copy=True)
    lead_time = fields.Integer('Lead Time', default=0, copy=True)

    @api.model
    def create(self, vals):
        # Created Task_id sequence to mapped depend_on_ids tasks
        if 'task_id' not in vals or vals.get('task_id') == _('New'):
            vals['task_id'] = self.env['ir.sequence'].next_by_code('project.task') or _('New')
        result = super(project_task, self).create(vals)
        return result

    @property
    def SELF_READABLE_FIELDS(self):
        """ Override this method to add task_id and lead_time as Readable Fields"""
        return super().SELF_READABLE_FIELDS | PROJECT_TASK_READABLE_FIELDS

class Project(models.Model):
    _inherit = 'project.project'

    @api.model
    def _map_tasks_default_valeus(self, task, project):
        """ get the default value for the copied task on project duplication """
        res = super(Project, self)._map_tasks_default_valeus(task, project)
        # Update lead_time and task_id as per template Tasks
        res.update({
            'lead_time' : task.lead_time,
            'task_id' : task.task_id
        })
        return res

    def map_tasks(self, new_project_id):
        res = super(Project, self).map_tasks(new_project_id)
        project = self.browse(new_project_id)
        # get Newly created tasks
        new_tasks_ids = project.tasks
        # get old task defined on Template
        old_task_ids = self.env['project.task'].with_context(active_test=False).search([('project_id', '=', self.id)],
                                                                                   order='parent_id')
        # Get task_id sequence for task and it's related depend_on_ids tasks
        old_depend_on_task_ids = {task.task_id: task.depend_on_ids.mapped('task_id') for task in old_task_ids if task.depend_on_ids}

        # Based on sequence task_id fetch new id of depend_on_ids task and set on task
        for new_task in new_tasks_ids:
            if new_task.task_id in old_depend_on_task_ids:
                old_depend_on_task_id = new_tasks_ids.filtered(lambda task: task.task_id in old_depend_on_task_ids[new_task.task_id])
                if old_depend_on_task_id:
                    # Write new task id for depend_on_ids field
                    new_task.depend_on_ids = [(6, 0, old_depend_on_task_id.ids)]
        return res

