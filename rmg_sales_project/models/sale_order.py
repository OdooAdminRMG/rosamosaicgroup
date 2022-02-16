# -*- coding: utf-8 -*-
from odoo import fields, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def calculate_planned_dates(self, commitment_date=False):
        def get_depend_on_task_list(final_task, all_task_list, planned_date_begin):
            depend_on_task_list = []
            planned_date_end = commitment_date
            while final_task:
                if final_task.id not in all_task_list:
                    planned_date_begin -= relativedelta(days=final_task.lead_time)
                    final_task.planned_date_begin = planned_date_begin
                    final_task.planned_date_end = planned_date_end
                    depend_on_task_list.append(final_task.id)
                final_task = final_task.depend_on_ids and final_task.depend_on_ids[0] or False
                planned_date_end = planned_date_begin
            return depend_on_task_list
        if commitment_date:
            for project in self.project_ids:
                all_task_list = []
                # get all depended_task_ids
                depended_task_ids = [depend_task for task in project.tasks for depend_task in task.depend_on_ids]
                # Manage final task by which doesn't set as depended_task
                final_task_ids = set(project.tasks) - set(depended_task_ids)
                for final_task in sorted(final_task_ids, key=lambda  x: x.sequence):
                    # so_commitment_date = datetime.strptime(commitment_date,'%Y-%m-%d %H:%M:%S')
                    final_task_depends_list = get_depend_on_task_list(final_task, all_task_list, commitment_date)
                    all_task_list.extend(final_task_depends_list)

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if 'commitment_date' in vals:
            self.calculate_planned_dates(vals['commitment_date'])
        return res

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.calculate_planned_dates(commitment_date=self.commitment_date)
        return res
