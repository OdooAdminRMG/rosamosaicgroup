# -*- coding: utf-8 -*-

from odoo import fields, models, api


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
        return res

    def write(self, vals):
        '''
         Override Write method  to check name of meeting include template or install
        '''
        res = super(ProjectTask, self).write(vals)
        if vals.get('name'):
            self.check_templating_installing()
        return res

    def check_templating_installing(self):
        '''
        Created Server Action to update old Record to check weather they include template or install in it
        '''
        for rec in self:
            name = rec.name and rec.name.lower() or ''
            rec.is_installing = True if 'install' in name else False
            rec.is_templating = True if 'template' in name else False
