from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)

class CSRDESRS(models.Model):
    _description = 'ESRS Datapoints'
    _inherit = 'csrd.esrs'

    uom_id = fields.Many2one(comodel_name="uom.uom")
    data_type = fields.Many2one(comodel_name="esrs.data.type")
    esrs_line_ids = fields.One2many(comodel_name="esrs.line", inverse_name="csrd_esrs_id")
    quantity = fields.Float(string="Data Value", compute="_compute_quantity")
    parent_id = fields.Many2one(comodel_name="csrd.esrs")
    child_ids = fields.One2many(comodel_name="csrd.esrs", inverse_name="parent_id")
    count_esrs_lines = fields.Integer(compute="_compute_count_esrs_lines")

    @api.depends("esrs_line_ids")
    def _compute_count_esrs_lines(self):
        for record in self:
            record.count_esrs_lines = len(record.esrs_line_ids)

    def get_children(self):
        self.ensure_one()
        action = {
            'name': 'ESRS_lines',
            'type': 'ir.actions.act_window',
            'res_model': 'esrs.line',
            'view_mode': 'tree',
            'target': 'current',
            'domain': [('id', 'in', self.esrs_line_ids.ids)]
        }
        return action

    def open_survey_wizard(self):
        self.ensure_one()
        if self.survey_id:
            return {
                'name': "Test Wizard",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'csrd.esrs.gather.survey.wizard',
                'context': {'default_survey_id': self.survey_id.id, 'default_csrd_esrs_id': self.id},
                'target': 'new',
            }

    def _compute_quantity(self):
        for record in self:
            record.quantity = sum(map(lambda esrs_line_id: esrs_line_id.quantity, record.esrs_line_ids))


    @api.onchange("parent_id")
    def set_category_on_childe(self):
        for record in self:
            record.category_id = record.parent_id.category_id
