odoo.define('rmg_sales_mrp.form_rendered', function(require) {
    "use strict";

    console.log("111111111111111111111")

    var FormRenderer = require('web.FormRenderer');
    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var viewRegistry = require('web.view_registry');
    var core = require('web.core');
    var _t = core._t;

    var RMGFormController = FormController.include({
        /**
        * Called when the user wants to save the current record -> @see saveRecord
        *
        * @private
        * @param {MouseEvent} ev
        */
        _onSave: function (ev) {
            ev.stopPropagation(); // Prevent x2m lines to be auto-saved
            // this._disableButtons();
            // this.saveRecord().then(this._enableButtons.bind(this)).guardedCatch(this._enableButtons.bind(this));
            // this._super.apply(this, arguments);
            if (this.modelName == "rmg.sale") {
                window.location.reload()
            }
            else {
                this._disableButtons();
                this.saveRecord().then(this._enableButtons.bind(this)).guardedCatch(this._enableButtons.bind(this));
            }
        },

    });

    var RMGFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: RMGFormController,
        }),
    });

    viewRegistry.add('rmg_form', RMGFormView);


});