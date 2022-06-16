odoo.define('rmg_binary_file_preview.rmg_binary_preview', function(require) {


    var BasicFields = require('web.basic_fields');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var file_data = undefined;
    var Viewer = require('rmg_curved_backend_theme.RmgListDocumentViewer');


    BasicFields.FieldBinaryFile.include({

        events: _.extend({}, BasicFields.FieldBinaryFile.prototype.events, {
            'click .rmg_binary_file_preview': "rmg_onAttachmentView",
        }),

        _render: function() {
            var self = this;
            self._super.apply(this, arguments);
            if (!self.res_id) {
                self.$el.css('cursor', 'not-allowed');
            } else {
                self.$el.css('cursor', 'pointer');
                self.$el.attr('title', 'Download');
            }
            if (self.recordData.id){
                self.$el.append(core.qweb.render("rmg_preview_button"));
            }
        },

        rmg_onAttachmentView: function(ev) {
            var self = this;
            try {
                ev.preventDefault();
                ev.stopPropagation();
                var rmg_mimetype = self.recordData.mimetype;

                function docView(file_data) {
                    if (file_data) {
                        var match = file_data.type.match("(image|video|application/pdf|text)");
                        if(match){
                            var attachment = [{
                                filename: file_data.name,
                                id: file_data.id,
                                is_main: false,
                                mimetype: file_data.type,
                                name: file_data.name,
                                type: file_data.type,
                                url: "/web/content/" + file_data.id + "?download=true",
                            }]
                            var activeAttachmentID = file_data.id;
                            var attachmentViewer = new Viewer(self,attachment,activeAttachmentID);
                            attachmentViewer.appendTo($('body'));
                        }
                        else{
                            alert('This file type can not be previewed.')
                        }
                    }
                }
                if (rmg_mimetype) {
                    file_data = {
                        'id': self.recordData.id,
                        'type': self.recordData.mimetype || 'application/octet-stream',
                        'name': self.recordData.name || self.recordData.display_name || "",
                    }
                    docView(file_data);
                } else {
                    var def = ajax.jsonRpc("/get/record/details", 'call', {
                        'res_id': self.res_id,
                        'model': self.model,
                        'size': self.value,
                        'res_field': self.name || self.field.string,
                    });
                    return $.when(def).then(function(vals) {
                        if (vals && vals.id) {
                            docView(vals);
                        } else {
                            alert('The preview of the file can not be generated as it does not exist in the Odoo file system (Attachments).')
                        }
                    });
                }
            } catch (err) {
                alert(err);
            }
        },
    });
});




