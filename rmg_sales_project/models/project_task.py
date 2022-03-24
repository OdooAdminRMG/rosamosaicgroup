# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    """

    """
    _inherit = 'project.task'

    peg_to_manufacturing_order = fields.Boolean(string="Pag To Manufacturing")
    production_ids = fields.One2many(
        'mrp.production', 'project_task_id', string='MOs')
    mrp_production_count = fields.Integer(
        compute='_compute_total_mrp_production', string='Total MOs')

    @api.onchange('peg_to_manufacturing_order')
    def _onchange_peg_to_manufacturing_order(self):
        """Onchange: _onchange_peg_to_manufacturing_order

        """
        task_id = self.search([
            ('project_id', '=', self.project_id.id),
            ('peg_to_manufacturing_order', '=', True),
            ('id', '!=', self._origin.id)
        ])
        if task_id:
            raise ValidationError(_(
                "Task '%s' is already set as the Manufacturing Order Peg for "
                "this Project.\nYou must first un-check its Peg to "
                "Manufacturing Order checkbox before attempting to set it on "
                "this task."
            ) % task_id.name)


    # show tree and form view based on production
    def action_open_associated_mos(self):
        """

        """
        action = self.env.ref(
                'mrp.mrp_production_action'
            ).read()[0]
        action['domain'] = [['id', 'in', self.production_ids.ids]]
        return action

    # show smart button count for mrp production
    @api.depends('production_ids')
    def _compute_total_mrp_production(self):
        """

        """
        self.mrp_production_count = len(self.production_ids)

    # create MO from project.task button
    def action_open_mos_to_associate_with_task(self):
        """

        """
        peg_to_mo_task_id = self.filtered(
            lambda task: task.peg_to_manufacturing_order
        )
        if not peg_to_mo_task_id:
            raise ValidationError(_(
                'Please Select Peg to Manufacturing Order is True.'
            ))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'name': 'Manufacturing Orders',
            'res_model': 'mrp.production',
            'view_id': self.env.ref(
                'rmg_sales_project.rmg_mrp_production_tree_view'
            ).id,
            'domain': [
                ('state', 'not in', ('done', 'cancel')),
                ('id', 'not in', peg_to_mo_task_id.production_ids.ids)
            ],
            'context': {'task_id': peg_to_mo_task_id.id},
            'target': 'new'
        }
