# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _


class ReportAccountAgedPartner(models.AbstractModel):
    _inherit = "account.aged.partner"

    def _get_sql(self):
        rtn = super(ReportAccountAgedPartner, self)._get_sql()
        miscellaneous_journal_id = self.env['account.journal'].search([('type', '=', 'general')]).ids
        if 'JOIN account_journal journal ON journal.id = account_move_line.journal_id' in rtn:
            query = rtn.split('JOIN account_journal journal ON journal.id = account_move_line.journal_id')
            query.insert(1,
                       'JOIN account_journal journal ON journal.id = account_move_line.journal_id  AND journal.id NOT IN ' + str(
                           tuple(miscellaneous_journal_id)))
        return ''.join(query)
