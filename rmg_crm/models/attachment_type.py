from odoo import _, fields, models


class IrAttachmentType(models.Model):
    _name = "ir.attachment.type"
    _description = "This model will define type of Attachments"
    _rec_name = "name"

    name = fields.Char(string=_("Name"), required=True)
