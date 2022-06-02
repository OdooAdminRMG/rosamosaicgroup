# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class JobCosting(models.Model):
    _name = "job.costing"
    _description = "Job Costing"

    job_id = fields.Many2one('job.costing', string=_("Job Id"))
    job_name = fields.Char(string=_("Job Name"))

    purchase_eff = fields.Float(string=_("Purchase Eff"), compute="_compute_purchase_eff")
    total_cost_of_components = fields.Float(string=_("Total Cost of Components"), compute="_compute_mrp_cost")
    project_cost = fields.Float(string=_("Project"), compute="_compute_project_cost")
    budgeted_labor_cost = fields.Float(compute='_compute_budgeted_labor_cost', string=_("Budgeted Labor Cost"))
    budgeted_material_cost = fields.Float(compute='_compute_budgeted_labor_cost', string=_("Budgeted Material Cost"))

    def _compute_purchase_eff(self):
        for rec in self:
            rec.purchase_eff = sum(
                rec.env['replenish.sources'].search(
                    [
                        ('job_name', '=', rec.job_name)
                    ]).mapped(lambda rs: rs.product_uom_qty * rs.price_unit))

    def _compute_mrp_cost(self):
        for rec in self:
            rec.total_cost_of_components = sum(
                map(
                    lambda val: val.get('total_cost', 0),
                    self.env['report.mrp_account_enterprise.mrp_cost_structure'].get_lines(
                        self.env['mrp.production'].search(
                            [
                                ('job_name', '=', rec.job_name),
                                ('state', '=', 'done')
                            ]))
                )
            )

    def _compute_project_cost(self):
        for rec in self:
            rec.project_cost = sum(
                self.env['project.task'].search(
                    [
                        ('job_name', '=', rec.job_name)
                    ]).mapped(
                    lambda task:
                    sum(
                        task.timesheet_ids.mapped(
                            lambda line: line.unit_amount * line.employee_id.timesheet_cost
                        )
                    )
                )
            )

    def _compute_budgeted_labor_cost(self):
        for rec in self:
            rec.budgeted_labor_cost = sum(self.env['sale.order'].search(
                [
                    ('job_name', '=', rec.job_name)
                ]).mapped('budgeted_labor_cost'))

    def _compute_budgeted_labor_cost(self):
        for rec in self:
            rec.budgeted_labor_cost = sum(self.env['sale.order'].search(
                [
                    ('job_name', '=', rec.job_name)
                ]).mapped('budgeted_labor_cost'))

    @api.model
    def create_job_costing_record(self):
        jc_job_names = self.env['job.costing'].search([]).mapped('job_name')
        self.env['sale.order'].search(
            [
                ('job_name', 'not in', jc_job_names)
            ]).mapped(
            lambda so: self.env['job.costing'].create({'job_name': so.job_name}))
        so_job_names = self.env['sale.order'].search([]).mapped('job_name')
        self.env['job.costing'].search(
            [
                ('job_name', 'not in', so_job_names)
            ]).unlink()

        return {
            'name': _('Job Costing Tree'),
            'type': 'ir.actions.act_window',
            'res_model': "job.costing",
            'view_mode': "tree",
            'view_id': self.env.ref("rmg_crm.job_costing_tree").id,
            'target': "current",
        }
