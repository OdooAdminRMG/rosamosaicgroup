
/* @odoo-module */

require('web.dom_ready');
import viewRegistry from 'web.view_registry';

const ProjectCalendarView = viewRegistry.get('project_calendar');
const ProjectCalendarController = ProjectCalendarView.prototype.config.Controller;
ProjectCalendarController.include({
    _renderButtonsParameters() {
        return Object.assign({}, this._super(...arguments), {scaleDrop: false});
    },
});