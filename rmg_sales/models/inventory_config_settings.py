# -*- coding: utf-8 -*-

from odoo import _, api, models, fields
from ast import literal_eval


class InventoryConfiguration(models.TransientModel):
    _inherit = "res.config.settings"

    manufacturing_order_report_id = fields.Many2one('ir.actions.report',
                                                    domain=[('model', 'like', 'mrp.production')],
                                                    string=_(
                                                        "Manufacturing Order Report for RMG Deliveries"))

    @api.model
    def get_values(self):
        res = super(InventoryConfiguration, self).get_values()
        manufacturing_order_report_id = self.env["ir.config_parameter"].get_param(
            "rmg_sales.manufacturing_order_report_id"
        )
        if manufacturing_order_report_id:
            res.update(
                manufacturing_order_report_id=int(manufacturing_order_report_id)
                # [
                #     (6, 0, int(manufacturing_order_report_id))
                # ],
            )

            print("\n\n\nman: ", manufacturing_order_report_id)
            print("\n\n\nres: ", res)
        return res

    def set_values(self):
        self.env["ir.config_parameter"].set_param(
            "rmg_sales.manufacturing_order_report_id",
            self.manufacturing_order_report_id.id,
        )
        return super(InventoryConfiguration, self).set_values()
