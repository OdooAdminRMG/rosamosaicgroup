# -*- coding: utf-8 -*-

import base64
import os

from odoo import fields, models
from PyPDF2 import PdfFileReader, PdfFileWriter


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    image_attachment_id = fields.Many2many("ir.attachment", string="Image Attachment")

    def attach_pdf_file(self, data=None):
        """
        This method will attach all images and pdf which are selected in 'images attachments' fields to the main report.
        """

        def append_pdf(input, output):
            [
                output.addPage(input.getPage(page_num))
                for page_num in range(input.numPages)
            ]

        output = PdfFileWriter()
        if (
            self.image_attachment_id.filtered(
                lambda l: l.mimetype in ["image/jpeg", "image/png", "application/pdf"]
            )
            or not self.image_attachment_id
        ):
            report = self.env.ref("rmg_mrp.action_report_rmg_mrp_production_order")
            if data:
                data.update({"from_method": True})
            main_content_pdf = report._render_qweb_pdf(self.ids, data=data)
            main_content_pdf_encode = base64.encodebytes(main_content_pdf[0])
            with open(
                os.path.expanduser("/tmp/line_{}.pdf".format(self.id)), "wb"
            ) as fout:
                fout.write(base64.decodebytes(main_content_pdf_encode))

            append_pdf(
                PdfFileReader(
                    open("/tmp/line_{}.pdf".format(self.id), "rb"), strict=False
                ),
                output,
            )
            os.remove("/tmp/line_{}.pdf".format(self.id))
        for pdf_attachment in self.image_attachment_id.filtered(
            lambda l: l.mimetype == "application/pdf"
        ):
            with open(
                os.path.expanduser("/tmp/line_{}.pdf".format(pdf_attachment.id)), "wb"
            ) as fout:
                fout.write(base64.decodebytes(pdf_attachment.datas))

            append_pdf(
                PdfFileReader(
                    open("/tmp/line_{}.pdf".format(pdf_attachment.id), "rb"),
                    strict=False,
                ),
                output,
            )
            os.remove("/tmp/line_{}.pdf".format(pdf_attachment.id))

        output.write(open("/tmp/CombinedPages.pdf", "wb"))
        output_file = open("/tmp/CombinedPages.pdf", "rb")
        output_byte = output_file.read()

        os.remove("/tmp/CombinedPages.pdf")

        return output_byte, "pdf"
