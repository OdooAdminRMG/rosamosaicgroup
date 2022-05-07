# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    is_templating = fields.Boolean()
    is_installing = fields.Boolean()

    @api.onchange('name')
    def _onchange_installing(self):
        if self.name:
            name = self.name.lower()
            self.is_installing = True if 'install' in name else False
            self.is_templating = True if 'template' in name else False

    def check_templating_installing(self):
        for rec in self:
            if rec.name:
                name = rec.name.lower()
                rec.is_installing = True if 'install' in name else False
                rec.is_templating = True if 'template' in name else False
