# -*- coding: utf-8 -*-

from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def open_message_wizard(self, message):
        context = dict(self._context)
        context.update({"default_sale_id": self.id, "default_message": message})
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order.confirm.wiz",
            "name": "Confirm Sale Order Delivery Date",
            "target": "new",
            "views": [(False, "form")],
            "view_mode": "form",
            "view_id": self.env.ref("rmg_sales.view_sale_order_confirm_wiz_form").id,
            # Set default sale_id and message
            "context": context,
        }

    def action_confirm(self):
        # Pass context from action_confirm button to open wizard for Delivery date confirmation
        copy_context = dict(self._context)
        if (
            "so_action_confirm_warning" in copy_context
            and copy_context.get("so_action_confirm_warning") == "warning_1"
        ):
            copy_context.update({"so_action_confirm_warning": "warning_2"})
            if not any(
                self.order_line.filtered(
                    lambda product: product.product_id.detailed_type == "service"
                    and product.product_id.service_policy == "delivered_timesheet"
                    and product.product_id.service_tracking
                    in ["task_in_project", "project_only"]
                )
            ):
                return self.with_context(copy_context).open_message_wizard(
                    "There were no products added to this Sales Order which will result in the generation of a project. You may still save this order, but you will need to add such a product at a later date. Are you sure you want to proceed"
                )
        if "so_action_confirm_warning" in copy_context and (
            copy_context.get("so_action_confirm_warning") == "warning_2"
        ):
            copy_context.update({"so_action_confirm_warning": "end"})
            message = (
                "This Sales Order’s Delivery Date is currently set to %s. "
                "Please confirm this is correct before proceeding"
                % self.commitment_date
            )
            return self.with_context(copy_context).open_message_wizard(message)

        return super(SaleOrder, self).action_confirm()
