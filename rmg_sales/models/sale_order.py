# -*- coding: utf-8 -*-

from odoo import _, models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


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
        if not self.partner_shipping_id:
            raise UserError(_("Delivery address is not set."))
        tz = self.env.context.get('tz') or self.env.user.tz or 'UTC'
        locale = self.env.context.get('lang') or self.env.user.lang or 'en_US'
        # Pass context from action_confirm button to open wizard for Delivery date confirmation
        copy_context = dict(self._context)
        if (
            "so_action_confirm_warning" in copy_context
            and copy_context.get("so_action_confirm_warning") == "warning_1"
        ):
            copy_context.update({"so_action_confirm_warning": "warning_2"})
            if not any(
                self.order_line.filtered(
                    lambda line: line.product_id.service_tracking
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
                % format_datetime(self.env, self.commitment_date, tz=tz)
            )
            return self.with_context(copy_context).open_message_wizard(message)

        return super(SaleOrder, self).action_confirm()

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        - Sales Team
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        self = self.with_company(self.company_id)

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.context.get('default_user_id', self.env.uid)
        if user_id and self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms'):
            if self.terms_type == 'html' and self.env.company.invoice_terms_html:
                baseurl = html_keep_url(self.get_base_url() + '/terms')
                values['note'] = _('Terms & Conditions: %s', baseurl)
            elif not is_html_empty(self.env.company.invoice_terms):
                values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms
        if not self.env.context.get('not_self_saleperson') or not self.team_id:
            values['team_id'] = self.env['crm.team'].with_context(
                default_team_id=self.partner_id.team_id.id
            )._get_default_team_id(domain=['|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)], user_id=user_id)
        self.update(values)