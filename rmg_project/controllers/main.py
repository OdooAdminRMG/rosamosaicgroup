from odoo import http

from odoo.addons.web.controllers.main import DataSet


class ResequenceDataset(DataSet):

	@http.route('/web/dataset/resequence', type='json', auth="user")
	def resequence(self, model, ids, field='sequence', offset=0):
		if model != 'project.project' and not self._context.get('search_default_groupby_stage', False):
			return super(ResequenceDataset, self).resequence()
		return True
