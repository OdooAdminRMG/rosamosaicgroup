# -*- coding: utf-8 -*-

import datetime

from odoo import _, api, fields, models, tools
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTS


class JobCostingReport(models.Model):
    _name = "job.costing.report"
    _order = "pct desc"
    _description = """
        The records of this module will be created or removed by the query written in search_read method.
    """

    sale_id = fields.Many2one("sale.order", string=_("Sale Order"), required=True)
    filter_id = fields.Many2one("job.costing.report.filter", string=_("Filter Id"))
    job_name = fields.Char(string=_("Job Name"), related="sale_id.job_name", store=True)
    so_create_date = fields.Datetime(
        string=_(" As Of Date"), help="This field will used to filter records"
    )
    compute_all_fields = fields.Char(
        compute="_compute_all_fields",
        help="This field is used to calculate all the fields",
    )
    contract_amount = fields.Float(
        string=_("Contract Amount"),
        help="Compute the sum of amount_total of all Sale Orders  based on 'Job Name' "
             "and 'End Date'(if end date filter is selected).",
    )
    billings_to_date = fields.Float(
        string=_("Billings To Date"),
        help="Compute the sum of 'Amount Total' of all Invoices whose related Sale Orders has the same 'Job Name'."
             "and 'End Date'(if end date filter is selected).",
    )
    remaining = fields.Float(
        string=_("Remaining"),
        help="Calculate the difference of 'Contract Amount' and 'Billings To Date'.",
    )
    total_cost_of_purchase = fields.Float(
        string=_("Total Cost Of Purchase"),
        help="Compute the sum of (Product Uom Qty * Unit Price) of all Replenish Histories based on 'Job Name'."
             "and 'End Date'(if end date filter is selected).",
    )
    total_cost_of_components = fields.Float(
        string=_("Total Cost Of Components"),
        help="Compute the sum of 'Total Cost' of all Manufacturing Orders based on Job name."
             "and 'End Date'(if end date filter is selected).",
    )
    total_cost_of_purchase_timesheet = fields.Float(
        string=_("Total Cost Of Timesheet"),
        help="Compute the sum of (Unit Amount * Timesheet Cost of that employee) of all Tasks  based on 'Job Name'."
             "and 'End Date'(if end date filter is selected).",
    )
    actual = fields.Float(
        string=_("Actual"),
        help="Compute the sum of 'Total Cost Of Purchase', 'Total Cost Of Components' and 'Total Cost Of Timesheet'",
    )
    budget = fields.Float(
        string=_("Budget"),
        help="Calculate the sum of 'Budgeted Labor Cost' and 'Budgeted Material Cost' based on 'Job Name'."
             "and 'End Date'(if end date filter is selected).",
    )
    pct = fields.Float(
        string=_("Pct"), help="Calculate the percentage of 'Actual' divide by 'Budget'."
    )
    overrun = fields.Float(
        string=_("Overrun"), help="Calculate the difference of 'Actual' and 'Budget'."
    )

    def calculate_values_from_sale_order(self):
        """
        This method will calculate values of fields which depends on sale order.
        """
        so = self.sale_id
        filter_date = self.filter_id.filter_date

        # Compute the sum of amount_total of all Sale Orders  based on 'Job Name' and 'End Date'.
        self.contract_amount, self.budget = (
            (so.amount_total, so.budgeted_labor_cost + so.budgeted_material_cost)
            if ((filter_date and so.create_date <= filter_date) or not filter_date)
            else (0, 0)
        )
    # code backup
    # If we get multiple sale orders with same job name then we can use below code.

    # def calculate_values_from_sale_order(self):
    #     """
    #         This method will calculate values of fields which depends on sale order
    #     """
    #     filter_date = self.filter_id.filter_date
    #     sale_orders = self.env['sale.order'].search(
    #         [
    #             ('job_name', '=', self.job_name)
    #         ]
    #     )
    #
    #     # Compute the sum of amount_total of all Sale Orders  based on 'Job Name' and 'End Date'.
    #     self.contract_amount = sum(
    #         sale_orders.mapped(
    #             lambda so: so.amount_total
    #             if (
    #                     (
    #                             filter_date
    #                             and so.create_date <= filter_date
    #                     )
    #                     or not filter_date
    #             )
    #             else 0
    #         )
    #     )
    #
    #     self.budget = sum(
    #         sale_orders.mapped(
    #             lambda so: so.budgeted_labor_cost + so.budgeted_material_cost
    #         )
    #     )

    def compute_billings_to_date(self):
        """
        Return the sum of amount_total of all invoices related to sale order.
        """
        filter_date = self.filter_id.filter_date
        return sum(
            self.env["account.move"]
            .search([("job_name", "=", self.job_name)])
            .mapped(
                lambda move: move.amount_total
                if (
                        (
                                filter_date
                                and move.invoice_date
                                and move.invoice_date <= filter_date.date()
                        )
                        or not filter_date
                )
                else 0
            )
        )

    def compute_actual(self):
        """
        This method will calculate and return sum of
        'Total Cost Of Purchase', 'Total Cost Of Components' and 'Total Cost Of Timesheet'
        based on 'job_name' and 'filter_date'.
        """
        filter_date = self.filter_id.filter_date
        job_name = self.job_name
        total_cost_of_purchase = 0
        for po in (
                self.env["replenish.sources"]
                        .search([("job_name", "=", job_name)])
                        .mapped("po_id")
        ):
            for prodict in list(set(po.replenish_source_ids.mapped("product_id.id"))):
                product_done_qty = sum(
                    po.picking_ids.mapped(
                        lambda picking: sum(
                            picking.move_ids_without_package.mapped(
                                lambda move: move.quantity_done
                                if move.product_id.id == prodict
                                else 0
                            )
                        )
                        if picking.state == "done"
                           and (
                                   (
                                           picking.date_done
                                           and filter_date
                                           and picking.date_done <= filter_date
                                   )
                                   or not filter_date
                           )
                        else 0
                    )
                )
                for replenish_id in po.replenish_source_ids.filtered(
                        lambda replenishment: replenishment.product_id.id == prodict
                ):
                    if replenish_id.product_uom_qty <= product_done_qty:
                        done_qty = replenish_id.product_uom_qty
                        product_done_qty -= replenish_id.product_uom_qty
                    else:
                        done_qty = product_done_qty
                        product_done_qty = 0
                    if replenish_id.job_name == job_name:
                        total_cost_of_purchase += done_qty * replenish_id.price_unit
        cal_actual = [
            sum(
                map(
                    lambda val: val.get("total_cost", 0),
                    self.env[
                        "report.mrp_account_enterprise.mrp_cost_structure"
                    ].get_lines(
                        self.env["mrp.production"]
                        .search(
                            [
                                ("job_name", "=", job_name),
                                ("state", "=", "done"),
                            ]
                        )
                        .filtered(
                            lambda mo: mo.date_finished <= filter_date
                            if filter_date and mo.date_finished
                            else True
                        )
                    ),
                )
            ),
            sum(
                self.env["project.task"]
                .search([("job_name", "=", job_name)])
                .mapped(
                    lambda task: sum(
                        task.timesheet_ids.mapped(
                            lambda line: line.unit_amount
                                         * line.employee_id.sudo().timesheet_cost
                            if (
                                    (
                                            filter_date
                                            and line.date
                                            and line.date <= filter_date.date()
                                    )
                                    or not filter_date
                            )
                            else 0
                        )
                    )
                )
            ),
        ]
        self.total_cost_of_purchase = total_cost_of_purchase
        self.total_cost_of_components = cal_actual[0]
        self.total_cost_of_purchase_timesheet = cal_actual[1]
        return sum(cal_actual) + total_cost_of_purchase

    @api.depends("filter_id.filter_date", "job_name")
    def _compute_all_fields(self):
        """
        This method will calculate all fields based on 'job_name' and 'filter_date'.
        """
        for rec in self:
            if not rec.filter_id:
                rec.filter_id = self.env["job.costing.report.filter"].search(
                    [], limit=1
                )
            rec.calculate_values_from_sale_order()
            billings_to_date = rec.compute_billings_to_date()
            rec.remaining = rec.contract_amount - billings_to_date
            actual = rec.compute_actual()
            budget = rec.budget
            rec.pct = float(actual / budget if budget else 0.0)
            rec.overrun = actual - budget
            rec.billings_to_date = billings_to_date
            rec.actual = actual
            rec.compute_all_fields = ""

    def calculate_filter_date_from_domain(self, domain):
        """
        Calculate and return minimum date from all the conditions from the domain with the field 'so_create_date'.
        """
        rtn_filter_date = False

        filter_date = [
            filter_val[2]
            for filter_val in domain
            if len(filter_val) == 3 and filter_val[0] == "so_create_date"
        ]
        if filter_date:
            min_date = min(filter_date)
            rtn_filter_date = (
                min_date
                if not rtn_filter_date
                else min(
                    [
                        datetime.datetime.strptime(min_date, DTS),
                        datetime.datetime.combine(
                            rtn_filter_date, datetime.datetime.min.time()
                        ),
                    ]
                )
            )
        return rtn_filter_date

    @api.model
    def search_read(
            self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs
    ):
        """
        This method will create or remove records on job_costing_report.
        This method will update 'filter_date' if user selects any custom filters of 'End Date'.
        """
        if self._name == "job.costing.report":
            self._cr.execute(
                """
                DELETE FROM %s
                WHERE sale_id IS NULL
            """
                % self._table
            )
            self._cr.execute(
                """
                INSERT INTO %s (sale_id, job_name, so_create_date)
                select
                id, job_name, create_date
                FROM sale_order
                WHERE id NOT IN (SELECT sale_id FROM job_costing_report) AND job_name != ''
            """
                % self._table
            )

        order = self._order
        rtn = super(JobCostingReport, self).search_read(
            domain=domain, fields=fields, offset=offset, limit=limit, order=order
        )
        custom_filter_date = (
            self.calculate_filter_date_from_domain(domain) if domain else False
        )
        filter_id = self.env["job.costing.report.filter"].search([], limit=1)
        if custom_filter_date != filter_id.filter_date:
            filter_id.filter_date = custom_filter_date
        return rtn

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """
        function to hide field from default filter
        """
        res = super(JobCostingReport, self).fields_get(allfields=allfields, attributes=attributes)
        fields_to_hide = ["create_date", "write_date"]
        for field in fields_to_hide:
            if res.get(field, False):
                res.get(field)["searchable"] = False  # hide from filter
        return res
