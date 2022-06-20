from odoo import _, fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    # Provide inverse relation to attachment type.
    type_id = fields.Many2one("attachment.type", string=_("Attachment Type"))
