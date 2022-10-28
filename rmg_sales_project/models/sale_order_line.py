# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def unlink(self):
        if self.project_id:
            # Standard odoo don't delete or archive project associated with order line.
            # So, in order to prevent single turn error we need to raise user error.
            raise UserError(_("You cannot delete a order line containing project. "
                              "You can either archive it or first delete its project."))
        return super(SaleOrderLine, self).unlink()

    def _timesheet_create_project(self):
        """ Generate project for the given so line, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        res = super(SaleOrderLine, self)._timesheet_create_project()
        for new_task in res.tasks:
            old_task = self.product_id.project_template_id.tasks.filtered(lambda x: x.name == new_task.name)
            new_task.write({'is_template_task': old_task.is_template_task,
                                'peg_to_delivery_order': old_task.peg_to_delivery_order,
                                'peg_to_manufacturing_order': old_task.peg_to_manufacturing_order})
        return res
