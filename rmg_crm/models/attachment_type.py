from odoo import _, fields, models


class IrAttachmentType(models.Model):
    _name = "attachment.type"
    _description = "Ir Attachment Type"
    _rec_name = "name"

    name = fields.Char(string=_("Name"), required=True)
