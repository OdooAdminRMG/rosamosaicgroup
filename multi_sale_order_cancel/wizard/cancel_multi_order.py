from odoo import api, models


class CancelMultiOrder(models.TransientModel):
    _name = "cancel.multi.order"
    _description = "Cancel Multi Order"


    def action_cancel(self):
        orders = self.env.context.get('active_ids')
        cancel_orders = self.env['sale.order'].browse(orders)
        for cancel_order in cancel_orders:
            cancel_order.action_cancel()
