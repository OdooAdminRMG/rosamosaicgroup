from odoo import models, fields


class Users(models.Model):
    _inherit = 'res.users'

    allow_preview = fields.Boolean(string='Allow Preview',
                                   help='It will allow the user to access all attachments')
