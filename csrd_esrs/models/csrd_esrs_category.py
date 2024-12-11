from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class CSRDESRSCategory(models.Model):
    _name = 'csrd.esrs.category'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'ESRS Categorys'

    name = fields.Char()
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one(comodel_name='csrd.esrs.category', string='Parent Category', index=True)
    csrd_esrs_ids = fields.One2many(comodel_name="csrd.esrs", inverse_name="category_id")

    number_of_children = fields.Integer(compute="compute_number_of_children")

    impact_materiality_description = fields.Text(string="Impact Materiality Description")
    financial_materiality_description = fields.Text(string="Financial Materiality Description")

    survey_id = fields.Many2one(comodel_name='survey.survey')

    impact_materiality = fields.Selection([
            ('1','1'), 
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6'),
            ('7','7'),
            ('8','8'),
            ('9','9'),
            ('10','10'),
            ], 
            string="Impact Materiality",
            default=None,
            group_operator="max"
            )

    financial_materiality = fields.Selection([
            ('1','1'), 
            ('2','2'),
            ('3','3'),
            ('4','4'),
            ('5','5'),
            ('6','6'),
            ('7','7'),
            ('8','8'),
            ('9','9'),
            ('10','10'),
            ], 
            string="Financial Materiality",
            default=None,
            group_operator="max"
            )
    
    priority = fields.Selection(selection=[("0","0"),("1","1")])

    
    def compute_number_of_children(self):

        self.number_of_children = self.search_count([("parent_id", "child_of", self.id),("id", "!=", self.id)])

    def get_subcategorys(self):
        
        return {
            "name": "Subcategorys",
            "type": "ir.actions.act_window",
            "res_model": "csrd.esrs.category",
            "views": [[False,"list"],[False,"form"]],
            "domain": [("parent_id", "child_of", self.id), ("id", "!=", self.id)],
        }
    
    def set_materiality_downward(self):

        children = self.search([("parent_id", "child_of", self.id)])

        for child in children:
            
            if child.id != self.id:

                _logger.error(f"{child.name=}"*50)

                child.impact_materiality = child.parent_id.impact_materiality
                child.financial_materiality = child.parent_id.financial_materiality
\No newline at end of file
