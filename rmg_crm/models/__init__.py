"""
    File             -->     Depends on
    attachment_type  -->     ir_attachment
    job_costing      -->     sale_order,replenish_sources
"""

from . import (
    crm_lead,
    ir_attachment,
    ir_attachment_type,
    mrp_production,
    project_project,
    replenish_sources,
    purchase_order,
    sale_order,
    stock_picking,
    stock_rule,
    account_move,
    job_costing,
)
