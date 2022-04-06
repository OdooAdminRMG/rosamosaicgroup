from odoo import _, api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    job_name = fields.Char(
        compute="_compute_project_name", string=_("Job Name"), store=True
    )

    @api.depends("sale_line_id.order_id.opportunity_id.name", "sale_line_id.order_id.job_name")
    def _compute_project_name(self):
        for project in self:
            project.job_name = project.sale_line_id.order_id.job_name
            if project.job_name:
                project.name = (
                        project.sale_line_id.order_id.name + " - " + project.job_name
                )
