from odoo import _, api, fields, models


class Stock(models.Model):
    _inherit = "stock.picking"

    job_name = fields.Char(string=_("Job Name"), related="sale_id.job_name", store=True)
