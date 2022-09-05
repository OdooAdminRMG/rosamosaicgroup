# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def unlink(self):
        if self.project_id:
            # Stander odoo don't delete or archive project associated with order line.
            # So, in order to prevent single turn error we need to raise user error to prevent.
            raise UserError(_("You cannot delete a order line containing project. "
                              "You can either archive it or first delete its project."))
        return super(SaleOrderLine, self).unlink()
