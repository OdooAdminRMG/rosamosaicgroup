# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _


class ReportAccountAgedPartner(models.AbstractModel):
    _inherit = "account.aged.partner"

    def _get_sql(self):
        rtn = super(ReportAccountAgedPartner, self)._get_sql()
        if 'JOIN account_move move ON account_move_line.move_id = move.id' in rtn:
            query = rtn.split('JOIN account_move move ON account_move_line.move_id = move.id')
            query.insert(1,
                         "JOIN account_move move ON account_move_line.move_id = move.id AND move.move_type IN ('in_invoice', 'out_invoice')")
        return ''.join(query)
