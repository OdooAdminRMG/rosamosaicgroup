from odoo import api, fields, models
from odoo.tools.translate import _


class EdgeProfiles(models.Model):
    _name = "edge.profiles"
    _description = "edge profiles"

    name = fields.Char(string=_("Name"))
    description = fields.Text(string=_("Description"))
