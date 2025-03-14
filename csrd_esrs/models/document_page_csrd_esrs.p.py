from odoo import models, fields, api

class DocumentCSRD(models.Model):
    _name = 'document.page.csrd.esrs'
    _description = 'Glue model between document.page and csrd.esrs'

    csrd_esrs_id = fields.Many2one(comodel_name="csrd.esrs")
    document_page_id = fields.Many2one(comodel_name="document.page")
