# -*- coding: utf-8 -*-
from odoo import fields, models, _
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTS
from pytz import timezone, UTC
from odoo.addons.resource.models.resource import float_to_time


import logging
_logger = logging.getLogger(__name__)


def get_next_or_last_working_days_count(date, attendance_ids, back_step=True):
    """

    :param date: Date which we need to check If it's holiday than step back or up and get new date which is in working hours
    :param attendance_ids: Working Hours
    :param back_step: Check If it's true then it will go backward else go forward
    :return: Date which is in working hours
    """
    if date.weekday() not in list(map(int, attendance_ids.mapped('dayofweek'))):
        return get_next_or_last_working_days_count((date - relativedelta(days=1)) if back_step else (date + relativedelta(days=1)), attendance_ids)
    return (date - relativedelta(days=1)) if back_step else (date + relativedelta(days=1))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_working_start_end_date(self, start_date, end_date):
        """

        :param start_date: task start date
        :param end_date: task end date
        :return: working hour start date, end date, all week records
        """
        resource_id = self.env.user.resource_ids[0] if self.env.user.resource_ids else self.env['resource.resource']
        working_start_date = datetime.combine(start_date.date(), time.min).replace(tzinfo=UTC)
        working_end_date = datetime.combine(end_date.date(), time.max).replace(tzinfo=UTC)
        work_intervals_batch = resource_id.calendar_id._work_intervals_batch(working_start_date, working_end_date, resources=resource_id)
        work_intervals = [(start, stop) for start, stop, dummy in work_intervals_batch.get(resource_id.id, False)]
        if work_intervals:
            working_start_date = work_intervals[0][0].astimezone(UTC)
            working_end_date = work_intervals[-1][-1].astimezone(UTC)

        return working_start_date, working_end_date, resource_id.calendar_id.attendance_ids

    def adjust_dates_in_user_working_time(self, start_date, end_date):
        """
            This method will get the resource calendar and calculate working time and adjust dates accordingly
            :param start_date: Task start date
            :param end_date: Task end date
            :return: adjusted start and end dates
        """
        start_date = start_date.replace(tzinfo=UTC)
        end_date = end_date.replace(tzinfo=UTC)
        working_start_date, working_end_date, all_attendance_ids = self.get_working_start_end_date(start_date, end_date)
        # Custom logic to adjust start date and end date in working time
        if start_date < working_start_date:
            start_date = get_next_or_last_working_days_count(working_end_date, all_attendance_ids) - (working_start_date - start_date)
            if end_date < working_start_date:
                end_date = working_start_date + (working_start_date - end_date)

        if end_date > working_end_date:
            end_date = get_next_or_last_working_days_count(working_start_date, all_attendance_ids, back_step=False) + (end_date - working_end_date)
            if start_date < working_end_date:
                start_date = working_end_date - (working_end_date - start_date)

        return start_date.astimezone(UTC).replace(tzinfo=None), end_date.astimezone(UTC).replace(tzinfo=None)

    def calculate_planned_dates(self, commitment_date):
        """
        Update task's start and end date
        :param commitment_date: Date from quotation deadline date
        :return: None
        """
        # Adjust the commitment date as per the working hours
        commitment_date, commitment_date = self.adjust_dates_in_user_working_time(commitment_date, commitment_date)

        def get_depend_on_task_list(final_task, task_depend_on_dict, commitment_date, previous_task):
            """
            Recursion method to update all child tasks
            :param final_task: Task in which start and end date should be placed
            :param task_depend_on_dict: dependent tasks' dictionary
            :param commitment_date: Deadline date
            :param previous_task: previous task to get offset hours
            :return: updated task
            """
            index = [final_task]
            if final_task and final_task in task_depend_on_dict:
                planned_date_begin_without_offset = commitment_date - relativedelta(hours=final_task.lead_time)
                planned_date_begin = planned_date_begin_without_offset - relativedelta(hours=previous_task.offset_hours or 0)
                # Check again start and end date because it may be possible that after subtracting start date may go beyond working time so setting as per the working hours
                date_begin, date_end = self.adjust_dates_in_user_working_time(planned_date_begin, commitment_date - relativedelta(hours=previous_task.offset_hours or 0))
                if not final_task.planned_date_begin or final_task.planned_date_begin > commitment_date:
                    final_task.planned_date_begin = date_begin
                    final_task.planned_date_end = date_end
                for inner_elem in task_depend_on_dict.get(final_task):
                    index.extend(get_depend_on_task_list(inner_elem, task_depend_on_dict, date_begin, previous_task=final_task))
            return index

        if commitment_date:
            for project in self.project_ids:
                all_task_list = []
                # get all depended_task_ids
                depended_task_ids = [depend_task for task in project.tasks for depend_task in task.depend_on_ids]
                task_depend_on_dict = {task: task.depend_on_ids for task in project.tasks}
                # Manage final task by which doesn't set as depended_task
                final_task_ids = set(project.tasks) - set(depended_task_ids)
                for final_task in sorted(final_task_ids, key=lambda x: x.sequence):
                    final_task_depends_list = get_depend_on_task_list(final_task, task_depend_on_dict, commitment_date, previous_task=self.env['project.task'])
                    all_task_list.extend(final_task_depends_list)

    def write(self, vals):
        """
        Override to update commitment date If changed and re-calculate
        :param vals: Values to write in task
        :return: Boolean
        """
        res = super(SaleOrder, self).write(vals)
        if 'commitment_date' in vals and vals['commitment_date']:
            so_commitment_date = datetime.strptime(vals['commitment_date'], DTS)
            self.calculate_planned_dates(so_commitment_date)
        return res

    def action_confirm(self):
        """
        Re-calculate planned dates on confirm of sales order
        :return:
        """
        res = super(SaleOrder, self).action_confirm()
        self.calculate_planned_dates(commitment_date=self.commitment_date)
        return res
