from odoo import fields, models
from odoo.tools.translate import _


class Faucets(models.Model):
    _name = "faucets"
    _description = "Faucets"

    name = fields.Char(string=_("Name"))
    description = fields.Text(string=_("Description"))
