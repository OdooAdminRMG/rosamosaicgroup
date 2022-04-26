
odoo.define('rmg_sales_mrp.section_rmg', function (require) {
// The goal of this file is to contain JS hacks related to allowing
// section and note on sale order and invoice.

// [UPDATED] now also allows configuring products on sale order.

"use strict";
var FieldChar = require('web.basic_fields').FieldChar;
var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
var fieldRegistry = require('web.field_registry');
var ListFieldText = require('web.basic_fields').ListFieldText;
var SectionRenderer = require('account.section_and_note_backend');
var rpc = require('web.rpc');

var SectionAndNoteListRendererAccount = SectionRenderer.include({
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

                var nbrColumns = this._getNumberOfCols();
                if (this.handleField) {
                    nbrColumns--;
                }
                if (this.addTrashIcon) {
                    nbrColumns--;
                }
                $cell.attr('colspan', nbrColumns);
            } else {
                if (record.model === "sale.order.line"){
                    var $button = $(
                        '\
                            <button type="button" title="Open section" style="float: right;" class="btn-primary oe_edit_only"> Selection Sheet\
                            </button>\
                        '
                    );
                    $cell.append($button);
                }
                $cell.removeClass('o_invisible_modifier');
                return $cell.addClass('o_hidden');
            }
        }

        return $cell;
    },

    _onClickOpen: function (ev) {
        var self = this;
        ev.stopPropagation();
        var $row = $(ev.target).closest('tr');
        var id = $row.data('id');
        var data = $(ev.target).closest('tr').find('.o_readonly_modifier')[0].innerText.trim()
        var myArray = data.split(" ");
        rpc.query({
            model: 'rmg.sale',
            method: 'search',
            args: [[['order_line_id', '=', parseInt(myArray)]]],
        })
        .then(function (rmgIds) {
            if (rmgIds.length > 0) {
                return self.do_action({
                    type: 'ir.actions.act_window',
                    name: 'RMG Selection Sheet',
                    res_model: 'rmg.sale',
                    views: [[false, 'form']],
                    target: 'new',
                    context: {
                        active_id: rmgIds[0],
                    },
                    res_id: rmgIds[0],
                    flags: {'action_buttons': true},
                });
            }
            else{
                return self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: 'rmg.sale',
                    name: 'RMG Selection Sheet',
                    views: [[false, 'form']],
                    target: 'new',
                    context: {
                        default_order_id: self.__parentedParent.res_id,
                        default_order_line_id: parseInt(myArray),
                        active_id: rmgIds[0],
                    },
                    flags: {'action_buttons': true},
                });
            }
        })
    },
});

});
