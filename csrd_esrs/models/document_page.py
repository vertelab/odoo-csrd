from odoo import models, fields, api

class DocumentCSRD(models.Model):
    _inherit = 'document.page'
    _description = 'Addeds a One2many filed connected to the glue model document.page.csrd'

    csrd_esrs_ids = fields.One2many(comodel_name="document.page.csrd.esrs", inverse_name="document_page_id")

    
