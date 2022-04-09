# -*- coding: utf-8 -*-
import logging

from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "hr.department"

    template_departments_id = fields.Many2one(
        "res.config.settings", string=_("Template Departments Id")
    )
