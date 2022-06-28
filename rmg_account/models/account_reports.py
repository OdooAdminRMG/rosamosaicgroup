# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'

    def _get_options(self, previous_options=None):
        # OVERRIDE
        options = super(AccountReport, self)._get_options(previous_options=previous_options)
        if self._name == 'account.aged.receivable' or self._name == 'account.aged.payable':
            options['remove_unknown_partners'] = previous_options and previous_options.get(
                'remove_unknown_partners') or False
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
        if self._context.get(
                'remove_unknown_partners',
                False
        ) and 'JOIN account_move move ON account_move_line.move_id = move.id' in rtn:
            query = rtn.split(
                'JOIN account_move move ON account_move_line.move_id = move.id'
            )
            query.insert(
                1,
                "JOIN account_move move "
                "ON account_move_line.move_id = move.id "
                "AND move.move_type IN ("
                "'in_invoice', "
                "'out_invoice', "
                "'out_refund', "
                "'in_refund'"
                ")"
            )
            return ''.join(query)
        return rtn
