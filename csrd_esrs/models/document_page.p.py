from odoo import models, fields, api

class DocumentCSRD(models.Model):
    _inherit = 'document.page'

    csrd_esrs_ids = fields.One2many(comodel_name="document.page.csrd.esrs", inverse_name="document_page_id")

    
