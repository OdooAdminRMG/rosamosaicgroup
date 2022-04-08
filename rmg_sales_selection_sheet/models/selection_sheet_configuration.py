from ast import literal_eval

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SelectionSheetConfiguration(models.TransientModel):
    _inherit = "res.config.settings"

    sink_by_bella_product_categories = fields.Many2many(
        "product.category",
        "product_category_rel",
        "categ_id",
        string=_("Sink by Bella Product Categories"),
    )
    template_departments = fields.Many2many(
        "hr.department", string=_("Template Departments")
    )
    companies = fields.Many2many("res.company", string=_("Companies"))

    @api.onchange("sink_by_bella_product_categories")
    def onchange_sink_by_bella_product_categories(self):
        for ele in self.sink_by_bella_product_categories:
            parent = ele
            while parent:
                if parent.parent_id in list:
                    raise UserError(
                        _(
                            "Select which Product Category nodes should be used as a filter for the Sink products selectable on the Selection Sheet"
                        )
                    )
                parent = parent.parent_id

    @api.model
    def get_values(self):
        res = super(SelectionSheetConfiguration, self).get_values()
        sink_by_bella_product_categories = self.env["ir.config_parameter"].get_param(
            "rmg_sales_selection_sheet.sink_by_bella_product_categories"
        )
        template_departments = self.env["ir.config_parameter"].get_param(
            "rmg_sales_selection_sheet.template_departments"
        )
        companies = self.env["ir.config_parameter"].get_param(
            "rmg_sales_selection_sheet.companies"
        )
        if sink_by_bella_product_categories:
            res.update(
                sink_by_bella_product_categories=[
                    (6, 0, literal_eval(sink_by_bella_product_categories))
                ],
            )
        if template_departments:
            res.update(
                template_departments=[(6, 0, literal_eval(template_departments))],
            )
        if companies:
            res.update(
                companies=[(6, 0, literal_eval(companies))],
            )
        return res

    def set_values(self):
        self.env["ir.config_parameter"].set_param(
            "rmg_sales_selection_sheet.sink_by_bella_product_categories",
            self.sink_by_bella_product_categories.ids,
        )
        self.env["ir.config_parameter"].set_param(
            "rmg_sales_selection_sheet.template_departments",
            self.template_departments.ids,
        )
        self.env["ir.config_parameter"].set_param(
            "rmg_sales_selection_sheet.companies", self.companies.ids
        )
        return super(SelectionSheetConfiguration, self).set_values()
