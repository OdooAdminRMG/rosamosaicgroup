from odoo import fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    is_req_email_confirm = fields.Boolean(string="request E-mail Confirmation", default=True)

    def send_activity_mail(self, state, subject):
        server_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        form_view = self.env['ir.ui.view'].search([('model', '=', self.res_model),
            ('type', '=', 'form')], limit=1)
        url = server_url + "/web?#id=%s&action_id=%s&model=%s" % (
                    self.res_id, form_view.id, self.res_model)
        template_id = self.env.ref("rmg_activity_confirmation.activity_confirmation")
        email_values = {
            "subject": "Activity " + subject,
            "email_from": self.create_uid.partner_id.email,
            "email_to": self.user_id.partner_id.email,
        }
        template_id.with_context(state=state, url=url).send_mail(
            self.id, force_send=True, email_values=email_values, notif_layout=False
        )

    def _action_done(self, feedback=False, attachment_ids=None):
        if self.is_req_email_confirm:
            self.send_activity_mail(state="Marked Done", subject="Completed")
        return super(MailActivity, self.with_context(done_activity=True))._action_done(feedback=feedback, attachment_ids=attachment_ids)

    def unlink(self):
        if self.is_req_email_confirm and not self._context.get('done_activity'):
            self.send_activity_mail(state="Marked Done", subject="Cancelled")
        return super(MailActivity, self).unlink()



