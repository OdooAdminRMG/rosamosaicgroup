from odoo import models, fields


class AddProduct(models.TransientModel):
    _name = 'add.product'
    _description = 'Add Product'

    product_id = fields.Many2one('product.product', string="Add new Product")
    so_line_id = fields.Many2one('sale.order.line')

    def replace_product(self):
        # Create new sale order line
        new_so_line = self.so_line_id.copy(default={'product_id':self.product_id.id,'order_id':self.so_line_id.order_id.id})
        new_so_line.write({'product_id': self.product_id.id})

        new_so_line.product_id_change()   #Call onchange for auto data fill

        self.so_line_id.write({'product_uom_qty': 0}) # update qty to zero
        self._cr.execute(f"""select id from stock_move where sale_line_id={self.so_line_id.id}""")
        picking_move_ids = list(map(lambda y: y[0], self._cr.fetchall()))

        procurement_groups = self.env['procurement.group'].search([('sale_id', 'in', self.so_line_id.order_id.ids)])
        mrp_production_ids = set(procurement_groups.stock_move_ids.created_production_id.ids) |\
            set(procurement_groups.mrp_production_ids.ids)

        mrp_list = []
        for mrp_production_id in mrp_production_ids:
            production = self.env['mrp.production'].browse(mrp_production_id)
            if production.sale_order_line_id and production.sale_order_line_id.order_id \
                    and production.sale_order_line_id.product_uom_qty != 0:
                production.procurement_group_id.sale_id = production.sale_order_line_id.order_id.id
            mrp_list.append(mrp_production_id)

        mrps = self.env['mrp.production'].browse(mrp_list)
        if self.so_line_id.product_id and self.so_line_id.product_uom_qty == 0 and mrps:
            mrp_pros = mrps.filtered(lambda l: l.sale_order_line_id.id == self.so_line_id.id)
            pick_ids = mrp_pros.mapped('picking_ids')
            if pick_ids:
                picking_move_ids.extend(pick_ids.mapped('move_lines').ids)
            mrp_pros.action_cancel()
        for move_id in picking_move_ids:
            move = self.env['stock.move'].browse(move_id)
            if move.picking_id.picking_type_code == 'outgoing':
                move.state = 'draft'
                move.unlink()
            elif move.state == 'done':
                if move.picking_id and move.picking_id.state == 'done' and \
                        not move.picking_id.picking_type_code == 'outgoing' and \
                        not move.picking_id.is_picking_returned:
                    wizard = self.env['stock.return.picking'].create({
                        'picking_id': move.picking_id.id
                    })
                    wizard.with_context({'manually_from_so': True})._onchange_picking_id()
                    new_picking_id, pick_type_id = wizard._create_returns()
                    move.picking_id.is_picking_returned = True
                    new_picking_rec = self.env['stock.picking'].browse(new_picking_id)
                    result = new_picking_rec.button_validate()
                    if isinstance(result, dict):
                        context = result.get("context")  # Merging dictionaries.
                        model = result.get("res_model", "")
                        # model can be stock.immediate.transfer or stock backorder.confirmation
                        if model:
                            record = self.env[model].with_context(context).create({})
                            record.process()
            else:
                if move.picking_id and len(move.picking_id.mapped('move_lines').ids) == 1:
                    move.picking_id.action_cancel()
                else:
                    move._action_cancel()
