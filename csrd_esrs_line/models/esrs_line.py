from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class ESRSLine(models.Model):
    _name = 'esrs.line'
    _description = 'Transaction line for esrs'

    name = fields.Char(compute="_compute_name", store=True)
    account_move_id = fields.Many2one(comodel_name="account.move")
    survey_id = fields.Many2one(comodel_name="survey.survey")
    csrd_esrs_id = fields.Many2one(comodel_name="csrd.esrs" )
    parent_csrd_esrs_id = fields.Many2one(comodel_name="csrd.esrs", related="csrd_esrs_id.parent_id", readonly=True, store=True)
    uom_id = fields.Many2one(comodel_name="uom.uom",compute="compute_uom_id")
    data_type = fields.Many2one(comodel_name="esrs.data.type",compute="compute_data_type")
    quantity = fields.Float(string="Quantity", required=True)
    
    @api.depends("csrd_esrs_id", "uom_id", "survey_id", "account_move_id", "account_move_id.name", "account_move_id.state")
    def _compute_name(self):
        for record in self:
            record.name = record.csrd_esrs_id.csrd_name if record.csrd_esrs_id else ""
            record.name = f"{record.name} ({record.uom_id.name})" if record.uom_id.name else record.name
            record.name = f"{record.name} ({record.account_move_id.name})" if record.account_move_id.name else record.name
            record.name = f"{record.name} ({record.survey_id.display_name})" if record.survey_id.display_name else record.name

    api.depends("csrd_esrs_id.uom_id")
    def compute_uom_id(self):
        for record in self:
            record.uom_id = record.csrd_esrs_id.uom_id

    api.depends("csrd_esrs_id.data_type")
    def compute_data_type(self):
        for record in self:
            record.data_type = record.csrd_esrs_id.data_type





