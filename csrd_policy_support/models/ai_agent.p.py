import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
  
_logger = logging.getLogger(__name__)

class AIAgent(models.Model):
    _inherit = 'ai.agent'
    
    ai_type = fields.Selection(selection_add=[('esrs_policy', 'ESRS Policy')],ondelete={'esrs_policy': 'cascade'})
