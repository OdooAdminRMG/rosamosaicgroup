# -*- coding: utf-8 -*-

from odoo import models, fields


class EditStockQuantWizard(models.TransientModel):
    _name = 'edit.stock.quant.wizard'
    _description = 'Edit Stock Quant Wizard'

    reserved_qty = fields.Float('Reserved Quantity', required=True)
    quant_id = fields.Many2one('stock.quant')

    def action_apply_reserved_qty(self):
        """
            Used to update reserved qty in stock quant.
        """
        self.quant_id.reserved_quantity = self.reserved_qty
