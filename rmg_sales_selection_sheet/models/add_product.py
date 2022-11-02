from odoo import models, fields


class AddProduct(models.TransientModel):
    _name = 'add.product'
    _description = 'Add Product'


    product_id=fields.Many2one('product.product',string="Add new Product")
    so_line_id = fields.Many2one('sale.order.line')

    def replace_product(self):
        # Create new sale order line
        new_so_line = self.so_line_id.copy(default={'product_id':self.product_id.id,'order_id':self.so_line_id.order_id.id})
        new_so_line.write({'product_id':self.product_id.id})

        new_so_line.product_id_change()   #Call onchange for auto data fill

        self.so_line_id.write({'product_uom_qty':0}) # update qty to zero
        self._cr.execute(f"""select id from stock_move where sale_line_id={self.so_line_id.id}""")
        picking_move_ids = list(map(lambda y: y[0], self._cr.fetchall()))

        procurement_groups = self.env['procurement.group'].search([('sale_id', 'in', self.so_line_id.order_id.ids)])
        mrp_production_ids = set(procurement_groups.stock_move_ids.created_production_id.ids) |\
            set(procurement_groups.mrp_production_ids.ids)

        mrp_list  = []
        for mrp_production_id in mrp_production_ids:
            mrp_list.append(mrp_production_id)

        mrps = self.env['mrp.production'].browse(mrp_list)
        if self.so_line_id.product_id and self.so_line_id.product_uom_qty == 0 and mrps:
            mrp_pros = mrps.search([('product_id','=',self.so_line_id.product_id.id)])
            mrp_pros.action_cancel()

        for move_id in picking_move_ids:
            move = self.env['stock.move'].browse(move_id)
            if move.picking_id.picking_type_code =='outgoing':
                move.state = 'draft'
                move.unlink()
            else:
                move.action_cancel()
        





