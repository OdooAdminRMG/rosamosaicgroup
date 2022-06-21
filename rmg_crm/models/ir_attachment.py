from odoo import _, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    type_id = fields.Many2one("ir.attachment.type", string=_("Attachment Type"))
