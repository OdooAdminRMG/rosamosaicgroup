from odoo import _, api, fields, models


class SelectionSheetConfiguration(models.TransientModel):
    _inherit = "res.config.settings"

    module_rmg_adjust_stock_valuation = fields.Boolean(string=_("Adjust Inventory Valuation"))

