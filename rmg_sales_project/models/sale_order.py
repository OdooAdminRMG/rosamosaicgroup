# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTS
from pytz import timezone, UTC

import logging

_logger = logging.getLogger(__name__)


def get_next_or_last_working_days_count(date, attendance_ids, back_step=True, recursive=False):
    """

    :param date: Date which we need to check If it's holiday than step back or up and get new date which is in working hours
    :param attendance_ids: Working Hours
    :param back_step: Check If it's true then it will go backward else go forward
    :return: Date which is in working hours
    """
    if date.weekday() not in list(map(int, attendance_ids.mapped('dayofweek'))):
        return get_next_or_last_working_days_count(
            (date - relativedelta(days=1)) if back_step else (date + relativedelta(days=1)), attendance_ids,
            recursive=True)
    if not recursive:
        date = (date - relativedelta(days=1)) if back_step else (date + relativedelta(days=1))
    return date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_project_product = fields.Boolean(string=_('is_project_product'), compute="_compute_is_project_product",
                                        store=True)

    @api.depends('order_line.product_id', 'order_line.project_id')
    def _compute_is_project_product(self):
        """
            The value of this filed will be True
            if any Sale Order Line exist with product type 'Service',
            'Create on Order' is not 'None' and  whose project doesn't exist else False.
        """
        for order in self:
            order.is_project_product = True if order.order_line.filtered(
                lambda line: line.product_id.detailed_type == 'service'
                             and line.product_id.service_tracking != 'no'
                             and not line.project_id) else False

    def action_create_project_confirm(self):
        for order in self:
            # All orders are in the same company
            orders = order.order_line.filtered(
                lambda line:
                line.product_id.detailed_type == 'service'
                and line.product_id.service_tracking != 'no'
                and not line.project_id
            )
            # check if all orders are in the same company
            # else Orders from different companies are confirmed together
            orders.sudo().with_company(self.company_id)._timesheet_service_generation() if len(
                self.company_id) == 1 else map(
                lambda order: order.order_line.sudo().with_company(
                    order.company_id
                )._timesheet_service_generation(),
                orders
            )
        if self.commitment_date:
            so_commitment_date = datetime.strptime(str(self.commitment_date), DTS)
            # Clear all dates on Project task
            for project in self.project_ids:
                project.tasks.planned_date_begin = False
                project.tasks.planned_date_end = False
            self.calculate_planned_dates(so_commitment_date)

    def get_attendances(self, start_date):
        resource_id = self.env.user.resource_ids[0] if self.env.user.resource_ids else self.env['resource.resource']
        attendances = resource_id.calendar_id.attendance_ids.filtered(
            lambda a: a.dayofweek == str(start_date.weekday()))
        return resource_id, attendances, resource_id.calendar_id.attendance_ids


    def get_start_date(self, start_date, hours):
        resource_id, attendances, all_attendance_ids = self.get_attendances(start_date)
        hours_per_day = resource_id.calendar_id._compute_hours_per_day(attendances)
        if hours >= hours_per_day:
            hours -= hours_per_day
            return self.get_start_date(get_next_or_last_working_days_count(start_date, all_attendance_ids), hours)
        start_date = self.adjust_dates_in_user_working_time(start_date - relativedelta(hours=hours), hours=hours)
        return start_date.replace(tzinfo=None)


    def get_working_start_end_date(self, start_date):
        """

        :param start_date: task start date
        :param end_date: task end date
        :return: working hour start date, end date, all week records
        """
        resource_id = self.env.user.resource_ids[0] if self.env.user.resource_ids else self.env['resource.resource']
        working_start_date = datetime.combine(start_date.date(), time.min).replace(tzinfo=UTC)
        working_end_date = datetime.combine(start_date.date(), time.max).replace(tzinfo=UTC)
        work_intervals_batch = resource_id.calendar_id._work_intervals_batch(working_start_date, working_end_date,
                                                                             resources=resource_id)
        work_intervals = [(start, stop) for start, stop, dummy in work_intervals_batch.get(resource_id.id, False)]
        if work_intervals:
            working_start_date = work_intervals[0][0].astimezone(UTC)
            working_end_date = work_intervals[-1][-1].astimezone(UTC)
        return working_start_date, working_end_date


    def adjust_dates_in_user_working_time(self, start_date, hours=0):
        """
            This method will get the resource calendar and calculate working time and adjust dates accordingly
            :param start_date: Task start date
            :param end_date: Task end date
            :return: adjusted start and end dates
        """
        start_date = start_date.replace(tzinfo=UTC)
        working_start_date, working_end_date = self.get_working_start_end_date(
            start_date.astimezone(timezone(self.env.user.tz)).replace(tzinfo=None))
        # Custom logic to adjust start date and end date in working time
        if start_date < working_start_date:
            resource_id, attendances, all_attendance_ids = self.get_attendances(start_date)
            if start_date.date() == working_start_date.date():
                last_day_start_date = get_next_or_last_working_days_count(start_date, all_attendance_ids)
            else:
                if start_date.weekday() not in list(map(int, all_attendance_ids.mapped('dayofweek'))):
                    last_day_start_date = get_next_or_last_working_days_count(start_date, all_attendance_ids)
                else:
                    last_day_start_date = start_date
            hours = (working_start_date - start_date).seconds / 3600
            working_start_date, working_end_date = self.get_working_start_end_date(last_day_start_date)
            start_date = working_end_date - relativedelta(hours=hours)

        return start_date.replace(tzinfo=None)


    def calculate_planned_dates(self, commitment_date):
        """
        Update task's start and end date
        :param commitment_date: Date from quotation deadline date
        :return: None
        """
        # Adjust the commitment date as per the working hours
        commitment_date = self.adjust_dates_in_user_working_time(commitment_date)

        def get_depend_on_task_list(final_task, task_depend_on_dict, commitment_date, first_task):
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
                # Check again start and end date because it may be possible that after subtracting start date may go beyond working time so setting as per the working hours
                date_end = self.get_start_date(commitment_date, final_task.offset_hours)
                date_begin = self.get_start_date(date_end if not first_task else commitment_date, final_task.lead_time)
                if not final_task.planned_date_begin or final_task.planned_date_begin > commitment_date:
                    final_task.planned_date_begin = date_begin
                    final_task.planned_date_end = commitment_date if first_task else date_end
                for inner_elem in task_depend_on_dict.get(final_task):
                    index.extend(get_depend_on_task_list(inner_elem, task_depend_on_dict, date_begin, first_task=False))
            return index

        if commitment_date:
            for project in self.project_ids:
                all_task_list = []
                # get all depended_task_ids
                depended_task_ids = [depend_task for task in project.tasks for depend_task in task.depend_on_ids]
                task_depend_on_dict = {task: task.depend_on_ids for task in project.tasks}
                # Manage final task by which doesn't set as depended_task
                final_task_ids = set(project.tasks) - set(depended_task_ids)
                for index, final_task in enumerate(sorted(final_task_ids, key=lambda x: x.sequence)):
                    final_task_depends_list = get_depend_on_task_list(final_task, task_depend_on_dict, commitment_date,
                                                                      first_task=True)
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
            # Clear all dates on Project task
            for project in self.project_ids:
                project.tasks.planned_date_begin = False
                project.tasks.planned_date_end = False
            self.calculate_planned_dates(so_commitment_date)
        return res


    def action_confirm(self):
        """
        Re-calculate planned dates on confirm of sales order
        :return:
        """
        res = super(SaleOrder, self).action_confirm()
        if self.commitment_date:
            self.calculate_planned_dates(commitment_date=self.commitment_date)
        project_task_mo = self.tasks_ids.filtered(
            lambda p: p.peg_to_manufacturing_order
        )
        project_task_do = self.tasks_ids.filtered(
            lambda p: p.peg_to_delivery_order
        )
        move_ids = self.env['procurement.group'].search([
            ('sale_id', 'in', self.ids)
        ]).stock_move_ids
        move_ids.created_production_id.project_task_id = project_task_mo.id
        picking_id = move_ids.picking_id.filtered(lambda x: x.picking_type_id.code == 'outgoing')
        picking_id.project_task_id = project_task_do.id
        if project_task_do.planned_date_end and picking_id:
            picking_id.scheduled_date = project_task_do.planned_date_end
            picking_id.date_deadline = project_task_do.planned_date_end
        if move_ids.created_production_id and project_task_mo.planned_date_begin and project_task_mo.planned_date_end:
            move_ids.created_production_id.date_planned_start = project_task_mo.planned_date_begin
            move_ids.created_production_id.date_deadline = project_task_mo.planned_date_end
        return res
