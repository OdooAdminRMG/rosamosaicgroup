from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    job_name = fields.Char(
        string=_("Job Name"), compute='_compute_job_name', store=True,
    )

    @api.depends('opportunity_id.name')
    def _compute_job_name(self):
        for rec in self:
            name = rec.opportunity_id.name
            if name:
                rec.job_name = name

