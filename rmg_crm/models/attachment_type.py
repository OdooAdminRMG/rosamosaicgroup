from odoo import _, fields, models


class IrAttachmentType(models.Model):
    _name = "ir.attachment.type"
    _description = "Ir Attachment Type"
    _rec_name = "name"
    # This model will define type of Attachments

    name = fields.Char(string=_("Name"), required=True)
