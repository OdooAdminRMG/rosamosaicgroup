from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    budgeted_labor_cost = fields.Float("Budgeted Labor Cost")
    budgeted_material_cost = fields.Float("Budgeted Material Cost")
    job_name = fields.Char(
        string=_("Job Name"),
        compute="_compute_job_name",
        store=True,compute_sudo=True
    )
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "rmg_sale_attachments_rel",
        compute="_compute_attachments",
        inverse="_inverse_attachments",
        readonly=False,
        store=True,compute_sudo=True
    )
    readonly_attachments = fields.Boolean(
        string=_("Readonly Attachments"),
        related="opportunity_id.readonly_attachments",
        invisible=True,
        help="Attachments will be readonly if any sale order related to opportunity will be in 'sale' state",
    )

    def _prepare_invoice(self):
        """Pass so_id from sale order to invoice."""
        rtn = super(SaleOrder, self)._prepare_invoice()
        rtn.update({"so_id": self.id})
        return rtn

    @api.depends("opportunity_id.name")
    def _compute_job_name(self):
        for rec in self:
            name = rec.opportunity_id.name
            if name:
                rec.job_name = name

    @api.depends("opportunity_id.attachment_ids")
    def _compute_attachments(self):
        for rec in self:
            rec.attachment_ids = rec.opportunity_id.attachment_ids.ids

    def _inverse_attachments(self):
        for rec in self:
            rec.opportunity_id.attachment_ids = rec.attachment_ids.ids

    def action_confirm(self):
        """
        -> While confirming the SO we have to create Replenish Source History for all SO Lines.
        -> For SO Lines which update the existing PO, we'll pass SO Line id to create Replenish Source History.
        """
        rtn = super(SaleOrder, self).action_confirm()
        for line in self.order_line:
            self._get_purchase_orders().filtered(
                lambda po: line.product_id.id in po.order_line.mapped("product_id.id")
                and line.id not in po.replenish_source_ids.mapped("so_line_id.id")
                and po.state in ["draft", "sent"]
            ).write({"replenish_source_ids": [(0, 0, {"so_line_id": line.id})]})
        return rtn


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _purchase_service_prepare_line_values(self, purchase_order, quantity=False):
        """
        This method is triggered when the SO Line will directly create PO
        and at that time we'll pass SO Line id to create Replenish Source History.
        """
        rtn = super(SaleOrderLine, self)._purchase_service_prepare_line_values(
            self, purchase_order, quantity
        )
        rtn.update({"replenish_source_ids": [(0, 0, {"so_line_id": self.id})]})
        return rtn

    def create(self, vals):
        """
        Override the default method to create Replenish Source History.
        -> When SO Line is created and the related SO is in 'sale' state
            and due to this line any PO is updated,
            we'll pass SO Line id to create Replenish Source History.
        """
        rtn = super(SaleOrderLine, self).create(vals)
        for line in rtn:
            line.order_id._get_purchase_orders().filtered(
                lambda po: line.product_id.id in po.order_line.mapped("product_id.id")
                and line.id not in po.replenish_source_ids.mapped("so_line_id.id")
                and po.state in ["draft", "sent"]
            ).write({"replenish_source_ids": [(0, 0, {"so_line_id": line.id})]})
        return rtn
