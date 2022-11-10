# -*- coding: utf-8 -*-


from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_picking_returned = fields.Boolean('Is Picking Returned?')
