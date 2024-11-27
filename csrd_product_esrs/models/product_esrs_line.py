from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProductESRSLine(models.Model):
    _name = 'product.esrs.line'
    _description = 'scaffold_test.scaffold_test'

    name = fields.Char()
    product_id = fields.Many2one(comodel_name="product.product")
    csrd_esrs_id = fields.Many2one(comodel_name="csrd.esrs")
    quantity = fields.Float()
    data_type = fields.Many2one(comodel_name="esrs.data.type")
    uom_id = fields.Many2one(comodel_name="uom.uom")

    api.depends("self.csrd_esrs_id.data_type")
    def compute_data_type(self):
        for record in self:
            record.data_type = record.csrd_esrs_id.data_type

    api.depends("self.csrd_esrs_id.uom_id")
    def compute_uom_id(self):
        for record in self:
            record.uom_id = record.csrd_esrs_id.uom_id


