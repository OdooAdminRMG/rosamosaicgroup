# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools


class JobCosting(models.Model):
    _name = "job.costing"
    _description = "Job Costing"
    _auto = False
    _log_access = True  # Include magic fields
    _rec_name = 'job_name'

    job_name = fields.Char(string=_("Job Name"))

    total_cost_of_purchase = fields.Float(
        string=_("Total Cost Of Purchase"),
        compute="_compute_actual",
        compute_sudo=True
    )
    total_cost_of_components = fields.Float(
        string=_("Total Cost Of Components"),
        compute="_compute_actual",
        compute_sudo=True
    )
    total_cost_of_purchase_timesheet = fields.Float(
        string=_("Total Cost Of Timesheet"),
        compute="_compute_actual"
    )
    # budgeted_labor_cost = fields.Float(
    # compute='_compute_contract_amount',
    # string=_("Budgeted Labor Cost")
    # )
    # budgeted_material_cost = fields.Float(
    # compute='_compute_contract_amount',
    # string=_("Budgeted Material Cost")
    # )
    contract_amount = fields.Float(
        compute='_compute_contract_amount',
        string=_("Contract Amount")
    )
    billings_to_date = fields.Float(
        compute='_compute_billings_to_date',
        string=_("Billings To Date")
    )
    remaining = fields.Float(
        compute='_compute_remaining',
        string=_("Remaining")
    )
    actual = fields.Float(
        compute='_compute_actual',
        string=_("Actual")
    )
    budget = fields.Float(
        compute='_compute_budget',
        string=_("Budget")
    )
    pct = fields.Float(
        compute='_compute_pct',
        string=_("Pct")
    )
    overrun = fields.Float(
        compute='_compute_overrun',
        string=_("Overrun")
    )

    def _compute_contract_amount(self):
        for rec in self:
            rec.contract_amount = sum(self.env['sale.order'].search(
                [
                    ('job_name', '=', rec.job_name)
                ]).mapped(lambda so: so.amount_total))

    def _compute_billings_to_date(self):
        for rec in self:
            rec.billings_to_date = sum(
                self.env['sale.order'].search(
                    [
                        ('job_name', '=', rec.job_name)
                    ]).mapped(
                    lambda so: sum(
                        so.order_line.invoice_lines.move_id.filtered(
                            lambda r: r.move_type in ('out_invoice', 'out_refund')
                        ).mapped('amount_total'))))

    def _compute_remaining(self):
        for rec in self:
            rec.remaining = rec.contract_amount - rec.billings_to_date

    def _compute_actual(self):
        for rec in self:
            cal_actual = [
                sum(
                    rec.env['replenish.sources'].search(
                        [
                            ('job_name', '=', rec.job_name)
                        ]).mapped(lambda rs: rs.product_uom_qty * rs.price_unit)),
                sum(
                    map(
                        lambda val: val.get('total_cost', 0),
                        self.env['report.mrp_account_enterprise.mrp_cost_structure'].get_lines(
                            self.env['mrp.production'].search(
                                [
                                    ('job_name', '=', rec.job_name),
                                    ('state', '=', 'done')
                                ]))
                    )
                ),
                sum(
                    self.env['project.task'].search(
                        [
                            ('job_name', '=', rec.job_name)
                        ]).mapped(
                        lambda task: sum(
                            task.timesheet_ids.mapped(
                                lambda line: line.unit_amount * line.employee_id.timesheet_cost
                            )
                        )
                    )
                )
            ]
            rec.total_cost_of_purchase = cal_actual[0]
            rec.total_cost_of_components = cal_actual[1]
            rec.total_cost_of_purchase_timesheet = cal_actual[2]
            rec.actual = sum(cal_actual)

    def _compute_budget(self):
        for rec in self:
            rec.budget = sum(
                [
                    sum(
                        self.env['sale.order'].search(
                            [
                                ('job_name', '=', rec.job_name)
                            ]
                        ).mapped('budgeted_labor_cost')
                    ),
                    sum(
                        self.env['sale.order'].search(
                            [
                                ('job_name', '=', rec.job_name)
                            ]
                        ).mapped('budgeted_labor_cost')
                    ),
                ]
            )

    def _compute_pct(self):
        for rec in self:
            budget = rec.budget
            rec.pct = float(rec.actual / budget if budget else 0.0)

    def _compute_overrun(self):
        for rec in self:
            rec.overrun = rec.actual - rec.budget

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
        CREATE or REPLACE VIEW %s AS
              select id,job_name  
              FROM sale_order WHERE job_name != ''
        """ % (self._table))
