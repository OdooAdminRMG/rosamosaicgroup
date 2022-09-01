# -*- coding: utf-8 -*-

import datetime

from odoo import _, api, fields, models, tools
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTS


class JobCostingReportFilter(models.Model):
    _name = "job.costing.report.filter"
    _description = """
        This model will only contain one record with one field name 'filter_date'.
        Value of 'filter_date' field will updated based on filter selected on 'job.costing.report'.
    """

    filter_date = fields.Datetime(
        string=_(" As Of Date"),
        help="This field will used to filter records of job_costing_report",
    )
