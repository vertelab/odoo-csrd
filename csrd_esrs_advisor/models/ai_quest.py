import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)
 
class AIQuest(models.Model):
    _inherit = 'ai.quest'
    
    ai_type = fields.Selection(selection_add=[('esrs_advisor', 'ESRS Advisor')],ondelete={'esrs_advisor': 'cascade'})

