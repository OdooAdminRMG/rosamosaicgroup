from odoo import api, fields, models
from odoo.tools.translate import _


class CornerTreatments(models.Model):
    _name = "corner.treatments"
    _description = "Corner Treatments"

    name = fields.Char(string=_("Name"))
    description = fields.Text(string=_("Description"))
