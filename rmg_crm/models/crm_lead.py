from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    # To resolve the uploading issue we have created Many2many field.
    attachment_ids = fields.Many2many(
        "ir.attachment", "rmg_crm_attachments_rel", string=_("Attachments")
    )

    readonly_attachments = fields.Boolean(
        string=_("Readonly Attachments"),
        compute="_compute_edit_attachments",
        invisible=True,
        help="Attachments will be readonly if any sale order related to opportunity will be in 'sale' state",
    )

    def _compute_edit_attachments(self):
        for rec in self:
            rec.readonly_attachments = any(
                rec.order_ids.filtered(lambda so: so.state in "sale")
            )

    def update_attachments(self):
        """
            This method will update attachments res_model, res_name, res_id.
        """
        for rec in self.env['project.project'].search([]):
            rec.attachment_ids.filtered(
                lambda attachment: attachment.write(
                    {'res_model': 'ir.attachment', 'res_id': rec.id, 'res_name': rec.name}
                )
            )
        for rec in self.search([]):
            rec.attachment_ids.filtered(
                lambda attachment: attachment.write(
                    {'res_model': 'ir.attachment', 'res_id': rec.id, 'res_name': rec.name}
                )
            )
