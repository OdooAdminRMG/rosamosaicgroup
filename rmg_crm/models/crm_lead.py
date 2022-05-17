from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    attachment_ids = fields.Many2many(
        "ir.attachment", "rmg_crm_attachments_rel", string=_("Attachments")
    )
    readonly_attachments = fields.Boolean(
        string=_("Readonly Attachments"),
        compute="_compute_edit_attachments",
        invisible=True,
    )

    def _compute_edit_attachments(self):
        for rec in self:
            rec.readonly_attachments = any(
                rec.order_ids.filtered(lambda so: so.state in "sale")
            )
