from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    job_name = fields.Char(
        string=_("Job Name"), related="opportunity_id.name", store=True
    )
