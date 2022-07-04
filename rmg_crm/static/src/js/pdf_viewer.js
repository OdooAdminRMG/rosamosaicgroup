
odoo.define('rmg_crm.pdf_viewer', function (require) {
"use strict";
var FieldChar = require('web.basic_fields').FieldChar;
var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
var fieldRegistry = require('web.field_registry');
var ListFieldText = require('web.basic_fields').ListFieldText;
var SectionRenderer = require('account.section_and_note_backend');
var rpc = require('web.rpc');

var SectionAndNoteListRendererAccount = ListFieldText.include({
    /**
     * We want section and note to take the whole line (except handle and trash)
     * to look better and to hide the unnecessary fields.
     *
     * @override
     */
    _renderBodyCell: function (record, node, index, options) {
        var $cell = this._super.apply(this, arguments);

        var isSection = record.data.display_type === 'line_section';
        var isNote = record.data.display_type === 'line_note';

        if (isSection || isNote) {
            if (node.attrs.widget === "handle") {
                return $cell;
            } else if (node.attrs.name === "name") {
                if (record.model === "sale.order.line"){
                    var $button = $(
                        '\
                            <button type="button" title="Open section" style="float: right;" class="btn-primary"> Selection Sheet\
                            </button>\
                        '
                    );



                this.getSession().user_has_group('sales_team.group_sale_manager').then(function(has_group){
                        if (has_group){
                    rpc.query({
                        model: 'ir.config_parameter',
                        method: "search_read",
                        args: [[['key', '=', 'rmg_sales_selection_sheet.companies']],["value"]],
                    }).then(function(data) {
                        if (eval(data[0].value).includes(record.data.company_id.data.id)) {
                            if (record.data.id ) {
                                $cell.append($button);
                            }
                        }

                    });
                        }
                    });
                    this.getSession().user_has_group('sales_team.group_sale_salesman').then(function(has_group){
                        if (has_group){
                    rpc.query({
                        model: 'ir.config_parameter',
                        method: "search_read",
                        args: [[['key', '=', 'rmg_sales_selection_sheet.companies']],["value"]],
                    }).then(function(data) {
                        if (eval(data[0].value).includes(record.data.company_id.data.id)) {
                            if (record.data.id ) {
                                $cell.append($button);
                            }
                        }

                    });
                        }
                    });
                    this.getSession().user_has_group('sales_team.group_sale_salesman_all_leads').then(function(has_group){
                        if (has_group){
                    rpc.query({
                        model: 'ir.config_parameter',
                        method: "search_read",
                        args: [[['key', '=', 'rmg_sales_selection_sheet.companies']],["value"]],
                    }).then(function(data) {
                        if (eval(data[0].value).includes(record.data.company_id.data.id)) {
                            if (record.data.id ) {
                                $cell.append($button);
                            }
                        }

                    });
                        }
                    });








                    $button.on('click', this._onClickOpen.bind(this));
                }













//odoo.define('rmg_crm.pdf_viewer', function (require) {
//"use strict";
//console.log('>>>>>>>>>>>>>>>>>>>>>>>>')
//"use strict";
//
//var rpc = require('web.rpc');
//
//$(document).on('click', '#pdf_viewer', function(){
//
//     console.log("test")
// });
//});
