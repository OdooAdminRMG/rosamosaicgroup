# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ReplenishSources(models.Model):
    _name = "replenish.sources"

    po_id = fields.Many2one("purchase.order", string=_("Purchase Order"), ondelete='cascade', invisible=True)
    so_line_id = fields.Many2one("sale.order.line", string=_("Sale Order Line"), ondelete='cascade', invisible=True)
    mo_id = fields.Many2one('mrp.production', compute='_compute_mo_id', string="Manufacturing Order", store=True,
                            ondelete='cascade', invisible=True)
    mo_origin = fields.Char(string=_('Manufacturing Origin'), invisible=True)

    so_id = fields.Many2one(related='so_line_id.order_id', string=_("Sale Order"), store=True, invisible=True)
    job_name = fields.Char(compute='_compute_replenish_sources_data', string=_("Job Name"), store=True)
    product_id = fields.Many2one('product.product', compute='_compute_replenish_sources_data', string=_("Product"),
                                 store=True)
    product_uom_qty = fields.Float(compute='_compute_replenish_sources_data', string=_("Quantity"), store=True)
    price_unit = fields.Float(compute='_compute_replenish_sources_data', string=_("Unit Price"), store=True)

    requested_by = fields.Many2one('res.users', default=lambda self: self.env.user, string=_('Requested By'))
    requested_on = fields.Datetime(string=_('Requested On'), default=lambda self: fields.Datetime.now())

    @api.depends('so_id.job_name', 'so_line_id.product_id','po_id.order_line.price_unit',
                 'so_line_id.product_uom_qty', 'mo_id.job_name','product_id.lst_price' )
    def _compute_replenish_sources_data(self):
        for rec in self:
            if rec.so_line_id:
                rec.job_name = rec.so_id.job_name
                rec.product_id = rec.so_line_id.product_id
                rec.product_uom_qty = rec.so_line_id.product_uom_qty
            else:
                rec.job_name = rec.mo_id.job_name
            rec.price_unit = rec.po_id.order_line.filtered(lambda po_line: po_line.product_id.id == rec.product_id.id).mapped('price_unit')[0]

    @api.depends('mo_origin')
    def _compute_mo_id(self):
        for rec in self:
            rec.mo_id = self.env['mrp.production'].search(
                [
                    ('name', '=', rec.mo_origin),
                ]).id
