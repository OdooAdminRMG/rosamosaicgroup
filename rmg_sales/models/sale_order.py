# -*- coding: utf-8 -*-

from odoo import _, api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        # Pass context from action_confirm button to open wizard for Delivery date confirmation
        if 'from_so_action_confirm' in self._context:
            message = "This Sales Order’s Delivery Date is currently set to %s. " \
                           "Please confirm this is correct before proceeding" % self.commitment_date
            return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.confirm.wiz',
            'name': 'Confirm Sale Order Delivery Date',
            'target': 'new',
            'views': [(False, 'form')],
            'view_mode': 'form',
            'view_id': self.env.ref('rmg_sales.view_sale_order_confirm_wiz_form').id,
            # Set default sale_id and message
            'context': {'default_sale_id': self.id, 'default_message': message}
        }
        return super(SaleOrder, self).action_confirm()




