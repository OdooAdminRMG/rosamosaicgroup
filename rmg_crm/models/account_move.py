# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    # Important: Run "Update Job Name In Existing Invoices" manually
    # to update sale id in those invoices which are created
    # before installation of this module

    so_id = fields.Many2one(
        "sale.order",
        string=_("Sale Order"),
    )
    job_name = fields.Char(
        string=_("Job Name"),
        compute="_compute_job_name",
        store=True,
    )

    @api.depends("so_id.job_name")
    def _compute_job_name(self):
        for rec in self:
            rec.job_name = rec.so_id.job_name

    def update_job_name_in_existing_invoices(self):
        """
        This scheduled action will update sale order id of all invoices.
        """
        self.env["sale.order"].search([]).mapped(
            lambda so: so.order_line.invoice_lines.move_id.filtered(
                lambda move: move.move_type in ("out_invoice", "out_refund")
            ).write({"so_id": so.id})
        )
