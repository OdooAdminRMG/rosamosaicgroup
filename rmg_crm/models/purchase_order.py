# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    replenish_source_ids = fields.One2many("replenish.sources",
                                           'po_id',
                                           string=_("Replenish Source Ids"),
                                           help=
                                           "Please run the scheduled action named "
                                           "'Create Replenish Sources History For Existing PO'"
                                           "manually (Only One Time) "
                                           "to create Replenish History for the records created before "
                                           "the installation of this module."
                                           )
