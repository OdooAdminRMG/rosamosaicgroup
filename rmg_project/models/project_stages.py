from odoo import api, fields, models


class ProjectStages(models.Model):
	_inherit = 'project.project.stage'

	sort_by_date = fields.Boolean(string="Sort By Date")

	@api.model_create_multi
	def create(self, vals_list):
		"""
			Override Create method to update sequence by stage's configuration
		"""
		res = super(ProjectStages, self).create(vals_list)
		self.env['project.project'].set_sequence(stage_id=res.id)
		return res

	def write(self, vals):
		"""
			Override write method to update sequence by stage's configuration
		"""
		res = super(ProjectStages, self).write(vals)
		if vals.get('sort_by_date', False):
			self.env['project.project'].set_sequence(stage_id=self.id)
		return res

