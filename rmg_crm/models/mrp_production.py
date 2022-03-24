from odoo import _, api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    job_name = fields.Char(string=_("Job Name"))

    @api.model
    def default_get(self, fields):
        print("\n\n\n\n\n inside default_get")
        return super(MrpProduction, self).default_get(fields)


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_mo_vals(
            self,
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
    ):
        rtn = super(StockRule, self)._prepare_mo_vals(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
            bom,
        )
        rtn["job_name"] = (
            self.env["sale.order"]
                .search([("name", "ilike", rtn.get("origin"))])
                .job_name
        )
        return rtn