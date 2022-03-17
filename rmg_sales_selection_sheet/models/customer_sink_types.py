from odoo import api, fields, models
from odoo.tools.translate import _


class CustomerSinkTypes(models.Model):
    _name = "customer.sink.types"
    _description = "customer sink types"

    name = fields.Char(string=_("Name"))
    description = fields.Text(string=_("Description"))
