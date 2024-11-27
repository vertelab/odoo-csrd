from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ESRSDataType(models.Model):
    _name = 'esrs.data.type'
    _description = 'Describes what type the ESRS datapoint refers to.'

    name = fields.Char()