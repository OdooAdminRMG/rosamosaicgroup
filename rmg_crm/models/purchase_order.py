# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    replenish_source_ids = fields.One2many("replenish.sources", 'po_id',
                                           string=_("Replenish Source Ids"))
