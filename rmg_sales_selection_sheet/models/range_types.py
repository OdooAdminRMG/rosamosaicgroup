from odoo import fields, models
from odoo.tools.translate import _


class RangeTypes(models.Model):
    _name = "range.types"
    _description = "range types"

    name = fields.Char(string=_("Name"))
    description = fields.Text(string=_("Description"))
