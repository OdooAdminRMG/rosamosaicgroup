from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    job_name = fields.Char(
        string=_("Job Name"),
        compute="_compute_job_name",
        store=True,
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "rmg_sale_attachments_rel",
        compute="_compute_attachments",
        inverse="_inverse_attachments",
        readonly=False,
        store=True,
    )
    readonly_attachments = fields.Boolean(
        string=_("Readonly Attachments"),
        related="opportunity_id.readonly_attachments",
        invisible=True,
    )

    @api.depends("opportunity_id.name")
    def _compute_job_name(self):
        for rec in self:
            name = rec.opportunity_id.name
            if name:
                rec.job_name = name

    @api.depends("opportunity_id.attachment_ids")
    def _compute_attachments(self):
        for rec in self:
            rec.attachment_ids = rec.opportunity_id.attachment_ids.ids

    def _inverse_attachments(self):
        for rec in self:
            rec.opportunity_id.attachment_ids = rec.attachment_ids.ids
