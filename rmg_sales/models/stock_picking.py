# -*- coding: utf-8 -*-

import base64
import os
from odoo import fields, models
from PyPDF2 import PdfFileReader, PdfFileWriter


class MrpProduction(models.Model):
    _inherit = "stock.picking"
    _description = "Stock Picking"

    def attach_pdf_file(self, data=None):
        """
        This method will attach all mrp reports which have job name = stock's job name
        and report template selected in res config settings to the rmg delivery slip's report.
        """

        def append_pdf(input, output):
            [
                output.addPage(input.getPage(page_num))
                for page_num in range(input.numPages)
            ]

        output = PdfFileWriter()
        report_id = int(
            self.env["ir.config_parameter"].sudo().get_param("rmg_sales.manufacturing_order_report_id")) if self.env[
            "ir.config_parameter"].sudo().get_param("rmg_sales.manufacturing_order_report_id") else False

        mrp_ids = self.env['mrp.production'].search(
            [('job_name', '=', self.job_name)]) if self.job_name and report_id else []

        stock_report_id = self.env['ir.actions.report'].search(
            [('report_name', '=', "rmg_sales.rmg_report_deliveryslip")]).id
        if data:
            data.update({"from_method": True})
        main_content_pdf = self.env['ir.actions.report'].browse(stock_report_id)._render_qweb_pdf(self.ids,
                                                                                                  data=data)
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
        # if mrp_ids:
        for pdf_attachment in mrp_ids:
            path = os.path.join("/tmp/")
            path += '/' + str(pdf_attachment) + '.pdf'

            temp = base64.b64encode(
                self.env['ir.actions.report'].browse(report_id)._render_qweb_pdf([pdf_attachment.id])[0])
            with open(
                    os.path.expanduser(path), "wb"
            ) as fout:
                fout.write(base64.decodebytes(temp))

            append_pdf(
                PdfFileReader(
                    open(path, "rb")
                ),
                output,
            )
            os.remove(path)

            if self.env['ir.actions.report'].browse(report_id).report_name == 'rmg_mrp.revised_mrp_production_template':
                for attachment in pdf_attachment.image_attachment_id.filtered(
                        lambda l: l.mimetype == "application/pdf"
                ):
                    path = os.path.join("/tmp")
                    path += '/' + str(attachment) + '.pdf'
                    with open(
                            os.path.expanduser(path), "wb"
                    ) as fout:
                        fout.write(base64.decodebytes(attachment.datas))

                    append_pdf(
                        PdfFileReader(
                            open(path, "rb"),
                            strict=False,
                        ),
                        output,
                    )
                    os.remove(path)

        output.write(open("/tmp/CombinedPages.pdf", "wb"))
        output_file = open("/tmp/CombinedPages.pdf", "rb")
        output_byte = output_file.read()
        os.remove("/tmp/CombinedPages.pdf")

        return output_byte, "pdf"
