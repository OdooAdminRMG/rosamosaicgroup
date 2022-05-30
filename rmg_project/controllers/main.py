from odoo.addons.web.controllers.main import DataSet
from odoo import http
from odoo.http import request


class ResequenceDataset(DataSet):

	@http.route('/web/dataset/resequence', type='json', auth="user")
	def resequence(self, model, ids, field='sequence', offset=0):
		if model != 'project.project' and hasattr(request, '_context') and not request._context.get('search_default_groupby_stage', False):
			return super(ResequenceDataset, self).resequence(model, ids, field, offset)
		return True
