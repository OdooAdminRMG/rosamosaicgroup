# -*- coding: utf-8 -*-
import logging

from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "hr.department"

    companies_id = fields.Many2one("res.config.settings", string=_("Companies Id"))
