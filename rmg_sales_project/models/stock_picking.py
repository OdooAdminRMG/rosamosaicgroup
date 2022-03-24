# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models


class StockPicking(models.Model):
    """

    """
    _inherit = "stock.picking"

    project_task_id = fields.Many2one('project.task', string="Project Task")
