# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    """

    """
    _inherit = 'project.task'

    peg_to_manufacturing_order = fields.Boolean(
        string="Pag To Manufacturing", copy=True)
    peg_to_delivery_order = fields.Boolean(
        string="Peg to Delivery Order", copy=True)
    production_ids = fields.One2many(
        'mrp.production', 'project_task_id', string='MOs')
    mrp_production_count = fields.Integer(
        compute='_compute_total_mrp_production', string='Total MOs')
    stock_picking_ids = fields.One2many(
        'stock.picking', 'project_task_id',
        string="Associated Delivery Order")
    picking_count = fields.Integer(string='Total Pickings',
                                   compute="_compute_picking_count")

    def _compute_picking_count(self):
        self.picking_count = len(self.stock_picking_ids)

    def get_tasks_for_associated(self, field, label):
        task_id = self.search([
            ('project_id', '=', self.project_id.id),
            (field, '=', True),
            ('id', '!=', self._origin.id)
        ])
        if len(task_id) > 1:
            raise ValidationError(_(
                "Task '%s' is already set as the %s Peg for "
                "this Project.\nYou must first un-check its Peg to "
                "%s checkbox before attempting to set it on this task."
            ) % task_id.name, label, label)

    @api.onchange('peg_to_manufacturing_order')
    def _onchange_peg_to_manufacturing_order(self):
        """Onchange: _onchange_peg_to_manufacturing_order

        """
        self.get_tasks_for_associated(
            field='peg_to_manufacturing_order',
            label='Manufacturing Order'
        )

    @api.onchange('peg_to_delivery_order')
    def _onchange_peg_to_delivery_order(self):
        """Onchange: _onchange_peg_to_delivery_order

        """
        self.get_tasks_for_associated(
            field='peg_to_delivery_order',
            label='Delivery Order'
        )

    def action_open_associated_pickings(self):
        """

        """
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['domain'] = [['id', 'in', self.stock_picking_ids.ids]]
        return action

    # show tree and form view based on production
    def action_open_associated_mos(self):
        """

        """
        action = self.env.ref('mrp.mrp_production_action').read()[0]
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

    def action_open_dos_to_associate_with_task(self):
        """

        """
        peg_to_do_task_id = self.filtered(
            lambda task: task.peg_to_delivery_order
        )
        if not peg_to_do_task_id:
            raise ValidationError(_(
                'Please Select Peg to Delivery Order is True.'
            ))
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'name': 'Transfers',
            'res_model': 'stock.picking',
            'view_id': self.env.ref(
                'rmg_sales_project.view_vpicktree_rmg_sale_projects'
            ).id,
            'domain': [
                ('state', 'not in', ('done', 'cancel')),
                ('id', 'not in', peg_to_do_task_id.stock_picking_ids.ids)
            ],
            'context': {'task_id': peg_to_do_task_id.id},
            'target': 'new'
        }
