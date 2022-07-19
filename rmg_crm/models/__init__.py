"""
    File             -->     Depends on
    attachment_type  -->     ir_attachment
    job_costing      -->     sale_order,replenish_sources
"""

from . import (account_move, attachment_type, crm_lead, ir_attachment,
               job_costing, mrp_production, project_project, purchase_order,
               replenish_sources, sale_order, stock_picking, stock_rule)
