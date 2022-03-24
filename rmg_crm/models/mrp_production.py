from odoo import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    job_name = fields.Char(string=_("Job Name"), compute="_compute_job_name", store=True)

    @api.depends('procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.job_name')
    def _compute_job_name(self):
        for rec in self:
            rec.job_name = rec.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.job_name
