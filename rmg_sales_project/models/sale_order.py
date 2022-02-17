# -*- coding: utf-8 -*-
from odoo import fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def calculate_planned_dates(self, commitment_date):
        def get_depend_on_task_list(final_task, task_depend_on_dict, commitment_date):
            index = [final_task]
            if final_task and final_task in task_depend_on_dict:
                planned_date_begin = commitment_date - relativedelta(days=final_task.lead_time)
                if not final_task.planned_date_begin or final_task.planned_date_begin > commitment_date:
                    final_task.planned_date_begin = planned_date_begin
                    final_task.planned_date_end = commitment_date
                for inner_elem in task_depend_on_dict.get(final_task):
                    index.extend(get_depend_on_task_list(inner_elem, task_depend_on_dict, planned_date_begin))
            return index

        if commitment_date:
            for project in self.project_ids:
                all_task_list = []
                # get all depended_task_ids
                depended_task_ids = [depend_task for task in project.tasks for depend_task in task.depend_on_ids]
                task_depend_on_dict = {task : task.depend_on_ids for task in project.tasks}
                # Manage final task by which doesn't set as depended_task
                final_task_ids = set(project.tasks) - set(depended_task_ids)
                for final_task in sorted(final_task_ids, key=lambda  x: x.sequence):
                    final_task_depends_list = get_depend_on_task_list(final_task, task_depend_on_dict, commitment_date)
                    all_task_list.extend(final_task_depends_list)

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if 'commitment_date' in vals:
            so_commitment_date = datetime.strptime(vals['commitment_date'], '%Y-%m-%d %H:%M:%S')
            self.calculate_planned_dates(so_commitment_date)
        return res

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.calculate_planned_dates(commitment_date=self.commitment_date)
        return res
