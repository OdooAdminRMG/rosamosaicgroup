# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    is_templating = fields.Boolean()
    is_installing = fields.Boolean()

    @api.onchange('name')
    def _onchange_installing(self):
        ''' Onchange method written to check name of meeting include template or install'''
        if self.name:
            name = self.name.lower()
            self.is_installing = True if 'install' in name else False
            self.is_templating = True if 'template' in name else False

    def check_templating_installing(self):
        ''' Created Server Action to update old Record to check wheather they nclude template or install in it'''
        for rec in self:
            if rec.name:
                name = rec.name.lower()
                rec.is_installing = True if 'install' in name else False
                rec.is_templating = True if 'template' in name else False
