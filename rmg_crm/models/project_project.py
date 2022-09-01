from odoo import _, api, fields, models


class Project(models.Model):
    _inherit = "project.project"

    job_name = fields.Char(
        compute="_compute_project_name",
        string=_("Job Name"),
        store=True,
        help="Compute 'Job Name' based on Opportunity's name of related Sale Order if exist else take 'Job Name' from related Sale Order.",
    )

    # To resolve the uploading issue we have created Many2many field.
    attachment_ids = fields.Many2many("ir.attachment", "rmg_project_attachments_rel")

    @api.depends(
        "sale_line_id.order_id.opportunity_id.name", "sale_line_id.order_id.job_name"
    )
    def _compute_project_name(self):
        """
        Project name should be concatenation of related Sale Order's 'name' and project's 'Job Name'.
        """
        for project in self:
            project.job_name = project.sale_line_id.order_id.job_name
            if project.job_name:
                project.name = (
                    project.sale_line_id.order_id.name + " - " + project.job_name
                )
            elif project.sale_line_id:
                project.sale_line_id.order_id.name

    @api.model
    def create(self, vals):
        """
        Extend the base method to set Attachments.
        """
        rtn = super(Project, self).create(vals)
        rtn.attachment_ids = rtn.sale_line_id.order_id.attachment_ids.ids
        return rtn


class ProjectTask(models.Model):
    _inherit = "project.task"

    job_name = fields.Char(
        related="project_id.job_name",
        string=_("Job Name"),
        store=True,
    )
