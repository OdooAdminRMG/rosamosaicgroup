odoo.define("rmg_curved_backend_theme.RmgListDocumentViewer", function (require) {
  "use strict";

  var core = require("web.core");
  var Widget = require("web.Widget");

  var QWeb = core.qweb;

  var RmgListDocumentViewer = Widget.extend({
    template: "rmg_curved_backend_theme.RmgListDocumentViewer",
    events: {
      "click .o_viewer_img": "OnImageClicked",
      "click .o_download_btn": "OnDownload",
      "click .o_viewer_video": "OnVideoController",
      "click .o_zoom_reset": "PreviewZoomReset",
      "click .o_rotate": "RotatePreview",
      "click .o_zoom_in": "PreviewZoomIn",
      "click .o_zoom_out": "_zoomOutPreview",
      "click .o_close_btn": "destroy",
      "click .o_print_btn": "_onPrintPreview",
      "DOMMouseScroll .o_viewer_content": "onScrollPreview",
      "mousewheel .o_viewer_content": "onScrollPreview",
      keyup: "onKeyUp",
    },

    /**
     * Initialize list document viewer.
     */
    init: function (parent, attachments, activeAttachmentID) {
      this._super.apply(this, arguments);
      this.attachment = _.filter(attachments, function (attachment) {
        if (attachment.type === "url")
          var match = attachment.url.match("(.png|.gif|youtu|.jpg)");
        else
          var match = attachment.mimetype.match(
            "(image|video|text|application/pdf)"
          );

        if (match) {
          attachment.fileType = match[1];
          if (match[1] === "youtu") {
            var youtube_arr = attachment.url.split("/");
            var youtube_token = youtube_arr[youtube_arr.length - 1];
            if (youtube_token.indexOf("watch") !== -1) {
              youtube_token = youtube_token.split("v=")[1];
              var amp = youtube_token.indexOf("&");
              if (amp !== -1) {
                youtube_token = youtube_token.substring(0, amp);
              }
            }
            attachment.youtube = youtube_token;
          }
          if (match[1].match("(.jpg|.png|.gif)")) {
            attachment.fileType = "image";
          }
          return true;
        }
      });
      this.activeAttachment = _.findWhere(attachments, {
        id: activeAttachmentID,
      });
      this.modelName = "ir.attachment";
      this.PreviewReset();
    },

    start: function () {
      this.$el.modal("show");
      this.$el.on("hidden.bs.modal", _.bind(this.onDestroy, this));
      this.$(".o_viewer_img").on("load", _.bind(this.onImageLoaded, this));
      this.$('[data-toggle="tooltip"]').tooltip({ delay: 0 });
      return this._super.apply(this, arguments);
    },

    destroy: function () {
      // Hide and remove modal.
      this.$el.modal("hide");
      this.$el.remove();
      // If preview is already destroyed.
      if (this.isDestroyed()) {
        return;
      }
      this._super.apply(this, arguments);
    },

    PreviewReset: function () {
      this.scale = 1;
      this.dragStartX = this.dragstopX = 0;
      this.dragStartY = this.dragstopY = 0;
    },

    previewGetTransform: function (scale, angle) {
      return (
        "scale3d(" + scale + ", " + scale + ", 1) rotate(" + angle + "deg)"
      );
    },

    previewRotate: function (angle) {
      this.PreviewReset();
      var new_angle = (this.angle || 0) + angle;
      this.$(".o_viewer_img").css(
        "transform",
        this.previewGetTransform(this.scale, new_angle)
      );
      this.$(".o_viewer_img").css(
        "max-width",
        new_angle % 180 !== 0 ? $(document).height() : "100%"
      );
      this.$(".o_viewer_img").css(
        "max-height",
        new_angle % 180 !== 0 ? $(document).width() : "100%"
      );
      this.angle = new_angle;
    },

    previewZoom: function (scale) {
      if (scale > 0.5) {
        this.$(".o_viewer_img").css(
          "transform",
          this.previewGetTransform(scale, this.angle || 0)
        );
        this.scale = scale;
      }
      this.$(".o_zoom_reset")
        .add(".o_zoom_out")
        .toggleClass("disabled", scale === 1);
    },

    onDestroy: function () {
      this.destroy();
    },

    /**
     * Handle download button.
     */
    OnDownload: function (ev) {
      ev.preventDefault();
      window.location =
        "/web/content/" +
        this.modelName +
        "/" +
        this.activeAttachment.id +
        "/" +
        "datas" +
        "?download=true";
    },

    /**
     * Handle print action.
     */
    _onPrintPreview: function (ev) {
      ev.preventDefault();
      var rmg_src = this.$(".o_viewer_img").prop("src");
      var script = QWeb.render("im_livechat.legacy.mail.PrintImage", {
        src: rmg_src,
      });
      var printWindow = window.open("about:blank", "_new");
      printWindow.document.open();
      printWindow.document.write(script);
      printWindow.document.close();
    },

    /**
     * Prevent image clicked.
     */
    OnImageClicked: function (ev) {
      ev.stopPropagation();
    },

    /**
     * Hide loader when after the image load.
     */
    onImageLoaded: function () {
      this.$(".o_loading_img").hide();
    },

    /**
     * Handle mouse zoom.
     *
     */
    onScrollPreview: function (ev) {
      var scale;
      if (ev.originalEvent.wheelDelta > 0 || ev.originalEvent.detail < 0) {
        scale = this.scale + 0.1;
        this.previewZoom(scale);
      } else {
        scale = this.scale - 0.1;
        this.previewZoom(scale);
      }
    },

    /**
     * Control media video.
     */
    OnVideoController: function (ev) {
      ev.stopPropagation();
      var videoElement = ev.target;
      if (videoElement.paused) {
        videoElement.play();
      } else {
        videoElement.pause();
      }
    },

    /**
     * Right rotate.
     */
    RotatePreview: function (ev) {
      ev.preventDefault();
      this.previewRotate(90);
    },

    /**
     * Reset preview content.
     */
    PreviewZoomReset: function (ev) {
      ev.preventDefault();
      this.$(".o_viewer_zoomer").css("transform", "");
      this.previewZoom(1);
    },

    /**
     * Handle zoom in functionality.
     */
    PreviewZoomIn: function (ev) {
      ev.preventDefault();
      var rmgScale = this.scale + 0.5;
      this.previewZoom(rmgScale);
    },

    /**
     * Handle zoom out functionality.
     */
    _zoomOutPreview: function (ev) {
      ev.preventDefault();
      var rmgScale = this.scale - 0.5;
      this.previewZoom(rmgScale);
    },

    onKeyUp: function (ev) {
      switch (ev.which) {
        case $.ui.keyCode.ESCAPE:
          ev.preventDefault();
          this.destroy();
          break;
      }
    },
  });

  return RmgListDocumentViewer;
});
