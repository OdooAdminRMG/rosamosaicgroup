from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, res_ids=None, data=None):
        """
        This method will override the base method is it is called from mrp else it will return super call.
        """
        if (
            self.model == "mrp.production"
            and self.report_file == "rmg_mrp.revised_mrp_production_template"
            and res_ids
            and data

            and not data.get("from_method")
        ):
            return (
                self.env["mrp.production"].browse(res_ids[0]).attach_pdf_file(data=data)
            )
        return super()._render_qweb_pdf(res_ids=res_ids, data=data)
