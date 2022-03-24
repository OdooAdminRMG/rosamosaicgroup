# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models


class StockPicking(models.Model):
    """

    """
    _inherit = "stock.picking"

    project_task_id = fields.Many2one('project.task', string="Project Task")

    # def action_confirm(self):
    #     # self._check_company()
    #     # self.mapped('package_level_ids').filtered(lambda pl: pl.state == 'draft' and not pl.move_ids)._generate_moves()
    #     # # call `_action_confirm` on every draft move
    #     # self.mapped('move_lines')\
    #     #     .filtered(lambda move: move.state == 'draft')\
    #     #     ._action_confirm()
    #     #
    #     # # run scheduler for moves forecasted to not have enough in stock
    #     # self.mapped('move_lines').filtered(lambda move: move.state not in ('draft', 'cancel', 'done'))._trigger_scheduler()
    #     # return True
    #     res = super(StockPicking, self).action_confirm()
    #     for rec in self:
    #         rec.project_task_id = rec.sale_id.tasks_ids.filtered(
    #             lambda task: task.peg_to_delivery_order
    #         ).id
    #         print("\n\n\n\n DO confirm rec.project_task_id :: ",rec.project_task_id, rec.sale_id, rec.sale_id.tasks_ids)
    #     return res
