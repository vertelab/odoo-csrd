from odoo import models, fields, api, _

import logging, os
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    ai_model = fields.Selection(selection=[["chatgpt","ChatGPT"],["mistral","Mistral"]])
    ai_api_key = fields.Char()
    ai_company_context = fields.Text(string="Ai Company Context")