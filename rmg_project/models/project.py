# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class Project(models.Model):
    _inherit = "project.project"

    def set_sequence(self, stage_id=False):
        """
            Method is responsible to set the proper sequence as per the stage's configuration
            :return:
        """
        stage_ids = self.stage_id.search([('sort_by_date', '=', True)] + ([('id', '=', stage_id)] if stage_id else []))
        for stage in stage_ids.filtered('sort_by_date').ids:
            project_ids = self.search([('stage_id', '=', stage)])
            has_expiration_date = project_ids.filtered('date').sorted('date')
            has_not_expiration_date = (project_ids - has_expiration_date)
            last_index = 0
            # Write the sequence for those project which has expiration date set
            for index, sorted_project in enumerate(has_expiration_date):
                sorted_project.write({'sequence': index})
                last_index = index
            # Write the sequence for those project which has no expiration date set
            for index, remaining_project in enumerate(has_not_expiration_date):
                remaining_project.write({'sequence': index + last_index + 1})

    def set_project_dates(self):
        """
            Method is responsible to set the project dates based on the tasks' deadlines
            :return: None
        """
        for project in self.filtered('task_ids'):
            task_planned_start_date = project.task_ids.filtered('planned_date_begin').mapped('planned_date_begin')
            task_planned_end_date = project.task_ids.filtered('planned_date_end').mapped('planned_date_end')
            project.write({
                'date_start': sorted(task_planned_start_date)[0] if task_planned_start_date else datetime.now(),
                'date': sorted(task_planned_end_date)[-1] if task_planned_end_date else datetime.now()
            })

    @api.model_create_multi
    def create(self, vals_list):
        """
            Override Create method to update sequence by stage's configuration
        """
        res = super(Project, self).create(vals_list)
        res.set_sequence(stage_id=res.stage_id.id)
        return res

    def write(self, vals):
        """
            Override write method to update sequence by stage's configuration
        """
        res = super(Project, self).write(vals)
        if vals.get('stage_id', False) or vals.get('date', False) or vals.get('date_start', False):
            self.set_sequence(stage_id=self.stage_id.id)
        return res


class ProjectTask(models.Model):
    _inherit = "project.task"

    is_templating = fields.Boolean()
    is_installing = fields.Boolean()

    @api.model_create_multi
    def create(self, vals_list):
        '''
         Override Create method  to check name of meeting include template or install

        '''
        res = super(ProjectTask, self).create(vals_list)
        res.check_templating_installing()
        if list(filter(lambda vals: vals.get('planned_date_begin', False) or vals.get('planned_date_end', False), vals_list)):
            res.project_id.set_project_dates()
        return res

    def write(self, vals):
        '''
         Override Write method  to check name of meeting include template or install
        '''
        res = super(ProjectTask, self).write(vals)
        if vals.get('name'):
            self.check_templating_installing()

        if vals.get('planned_date_begin', False) or vals.get('planned_date_end', False):
            self.project_id.set_project_dates()
        return res

    def check_templating_installing(self):
        '''
        Created Server Action to update old Record to check weather they include template or install in it
        '''
        for rec in self:
            name = rec.name and rec.name.lower() or ''
            rec.is_installing = True if 'install' in name else False
            rec.is_templating = True if 'template' in name else False
