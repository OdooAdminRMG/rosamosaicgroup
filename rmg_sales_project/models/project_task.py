# -*- coding: utf-8 -*-
# Part of Odoo, S4 Solutions, LLC.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

PROJECT_TASK_READABLE_FIELDS = {'task_id', 'lead_time', 'offset_hours'}
PROJECT_TASK_WRITABLE_FIELDS = {'offset_hours'}


class ProjectTask(models.Model):
    """

    """
    _inherit = 'project.task'

    peg_to_manufacturing_order = fields.Boolean(
        string="Peg To Manufacturing", copy=True)
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
    task_id = fields.Char(
        string='Task ID',
        default=lambda self: _('New'),
        copy=True)
    lead_time = fields.Integer('Lead Time', default=0, copy=True)
    offset_hours = fields.Integer('Offset Hours', default=0, copy=True)
    delivery_address_id = fields.Many2one("res.partner", string=_("Delivery Address"))
    overall_square_feet = fields.Float(string=_('Overall Square Feet'),
                                       compute="_compute_overall_square_feet")

    def _compute_overall_square_feet(self):
        for rec in self:
            rec.overall_square_feet = sum(
                rec.project_id.sale_line_id.order_id.order_line.mapped('rmg_sale_id.installed_square_footage'))

    @api.model
    def create(self, vals):
        # Created Task_id sequence to mapped depend_on_ids tasks
        if 'task_id' not in vals or vals.get('task_id') == _('New'):
            vals['task_id'] = self.env['ir.sequence'].next_by_code('project.task') or _('New')
        result = super(ProjectTask, self).create(vals)
        return result

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        mo_task = self.filtered(lambda x: x.peg_to_manufacturing_order)
        do_task = self.filtered(lambda x: x.peg_to_delivery_order)
        if 'planned_date_begin' in vals and vals['planned_date_begin']:
            if mo_task and mo_task.production_ids:
                mo_orders = mo_task.production_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                mo_orders.date_planned_start = mo_task.planned_date_begin
        if 'planned_date_end' in vals and vals['planned_date_end']:
            if mo_task and mo_task.production_ids:
                mo_orders = mo_task.production_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
                mo_orders.date_deadline = mo_task.planned_date_end
            if do_task and do_task.stock_picking_ids:
                do_task.stock_picking_ids.scheduled_date = do_task.planned_date_end
                do_task.stock_picking_ids.date_deadline = do_task.planned_date_end
        return res

    @property
    def SELF_READABLE_FIELDS(self):
        """ Override this method to add task_id and lead_time as Readable Fields"""
        return super().SELF_READABLE_FIELDS | PROJECT_TASK_READABLE_FIELDS

    @property
    def SELF_WRITABLE_FIELDS(self):
        """ Override this method to add offset hours in task from template"""
        return super(ProjectTask, self).SELF_WRITABLE_FIELDS | PROJECT_TASK_WRITABLE_FIELDS

    def _compute_picking_count(self):
        self.picking_count = len(self.stock_picking_ids)

    def get_tasks_for_associated(self, field, label):
        task_id = self.search([
            ('project_id', '=', self.project_id.id),
            (field, '=', True),
            ('id', '!=', self._origin.id)
        ])
        if task_id:
            raise ValidationError(_(
                "Task {task_name} is already set as the {label} Peg for "
                "this Project.\nYou must first un-check its Peg to "
                "{label} checkbox before attempting to set it on this task."
            ).format(task_name=task_id.name, label=label))

    @api.onchange('peg_to_manufacturing_order')
    def _onchange_peg_to_manufacturing_order(self):
        """Onchange: _onchange_peg_to_manufacturing_order

        """
        if self.peg_to_manufacturing_order:
            self.get_tasks_for_associated(
                field='peg_to_manufacturing_order',
                label='Manufacturing Order'
            )

    @api.onchange('peg_to_delivery_order')
    def _onchange_peg_to_delivery_order(self):
        """Onchange: _onchange_peg_to_delivery_order

        """
        if self.peg_to_delivery_order:
            self.get_tasks_for_associated(
                field='peg_to_delivery_order',
                label='Delivery Order'
            )

    def action_open_associated_pickings(self):
        """

        """
        action = self.env.ref('stock.action_picking_tree_all').sudo().read()[0]
        action['domain'] = [['id', 'in', self.stock_picking_ids.ids]]
        return action

    # show tree and form view based on production
    def action_open_associated_mos(self):
        """

        """
        action = self.env.ref('mrp.mrp_production_action').sudo().read()[0]
        action['domain'] = [['id', 'in', self.production_ids.ids]]
        return action

    # show smart button count for mrp production
    @api.depends('production_ids')
    def _compute_total_mrp_production(self):
        """

        """
        self.mrp_production_count = len(self.production_ids)

    # create MO from project.task button
    def open_mos_to_associate_with_task(self):
        """

        """
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
                ('id', 'not in', self.production_ids.ids)
            ],
            'context': {'task_id': self.id},
            'target': 'new'
        }

    def open_dos_to_associate_with_task(self):
        """

        """
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
                ('picking_type_id.code', '=', 'outgoing'),
                ('id', 'not in', self.stock_picking_ids.ids)
            ],
            'context': {'task_id': self.id},
            'target': 'new'
        }