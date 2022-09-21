from odoo import api, fields, models
from odoo.tools.translate import _


class CustomerSinkTypes(models.Model):
    _name = "customer.sink.types"
    _description = "Customer Sink Types"

    name = fields.Char(string=_("Name"))
    description = fields.Text(string=_("Description"))
