# -*- coding: utf-8 -*-


from odoo import _, api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    manufacturing_order_report_id = fields.Many2one('ir.actions.report',
                                                    domain=[('model', 'like', 'mrp.production')],
                                                    string=_(
                                                        "Manufacturing Order Report for RMG Deliveries"))
    suppresss_upsell_notification = fields.Boolean(string=_(
            "Suppress upsell notifications for project-linked products"))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        manufacturing_order_report_id = self.env["ir.config_parameter"].get_param(
            "rmg_sales.manufacturing_order_report_id"
        )
        is_suppress = self.env["ir.config_parameter"].get_param(
            "rmg_sales.suppresss_upsell_notification"
        )
        if manufacturing_order_report_id:
            res.update(
                manufacturing_order_report_id=int(manufacturing_order_report_id),
                suppresss_upsell_notification=is_suppress
            )

        return res

    def set_values(self):
        self.env["ir.config_parameter"].set_param(
            "rmg_sales.manufacturing_order_report_id",
            self.manufacturing_order_report_id.id,
        )
        self.env["ir.config_parameter"].set_param(
            "rmg_sales.suppresss_upsell_notification",
            self.suppresss_upsell_notification,
        )
        return super(ResConfigSettings, self).set_values()
