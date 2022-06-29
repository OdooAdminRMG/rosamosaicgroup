# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ReportAccountAgedReceivable(models.Model):
    _inherit = "account.aged.receivable"

    def _get_options(self, previous_options=None):
        # OVERRIDE
        options = super(ReportAccountAgedReceivable, self)._get_options(previous_options=previous_options)
        options['display_unknown_partners'] = previous_options and previous_options.get(
            'display_unknown_partners') or False
        return options


class ReportAccountAgedPayable(models.Model):
    _inherit = "account.aged.payable"

    def _get_options(self, previous_options=None):
        # OVERRIDE
        options = super(ReportAccountAgedPayable, self)._get_options(previous_options=previous_options)
        options['display_unknown_partners'] = previous_options and previous_options.get(
            'display_unknown_partners') or False
        return options


class ReportAccountAgedPartner(models.AbstractModel):
    _inherit = "account.aged.partner"

    def _get_sql(self):
        """
            based on context this method will override base method and modify query.
        """
        rtn = super(
            ReportAccountAgedPartner,
            self
        )._get_sql()
        if not self._context.get('report_options', {}
                                 ).get(
            'display_unknown_partners', False
        ) and 'WHERE account.internal_type = ' in rtn:
            query = rtn.split(
                'WHERE account.internal_type = '
            )
            query.insert(
                1,
                "WHERE account_move_line.partner_id IS NOT NULL AND account.internal_type = "
            )
            return ''.join(query)
        return rtn
