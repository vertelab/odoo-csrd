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
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('10', '10'),
    ], string="Impact Materiality", default=None, aggregator="max", group_expand='_read_group_impact_materiality')

    financial_materiality = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('10', '10'),
    ], string="Financial Materiality", default=None, aggregator="max",
        group_expand='_read_group_financial_materiality')
    
    priority = fields.Selection(selection=[("0","0"),("1","1")])

    @api.model
    def _read_group_impact_materiality(self, values, domain, order):
        all_values = [value[0] for value in self._fields['impact_materiality'].selection]

        # Make sure values contains all possible selection values
        missing_values = set(all_values) - set(values)
        values = values + list(missing_values)

        # Sort values numerically
        values.sort(key=lambda x: int(x) if x else 0)
        return values

    @api.model
    def _read_group_financial_materiality(self, values, domain, order):
        all_values = [value[0] for value in self._fields['financial_materiality'].selection]

        missing_values = set(all_values) - set(values)
        values = values + list(missing_values)

        # Sort values numerically
        values.sort(key=lambda x: int(x) if x else 0)
        return values

    def compute_number_of_children(self):
        for rec in self:
            rec.number_of_children = self.search_count([("parent_id", "child_of", rec.id),("id", "!=", rec.id)])

    def get_subcategorys(self):
        return {
            "name": "Subcategorys",
            "type": "ir.actions.act_window",
            "res_model": "csrd.esrs.category",
            "views": [[False,"tree"],[False,"form"]],
            "domain": [("parent_id", "child_of", self.id), ("id", "!=", self.id)],
        }
    
    def set_materiality_downward(self):
        children = self.search([("parent_id", "child_of", self.id)])
        for child in children:
            if child.id != self.id:
                child.impact_materiality = child.parent_id.impact_materiality
                child.financial_materiality = child.parent_id.financial_materiality

    def _get_csrd_category_lines(self, category_id):
        csrd_esrs_ids = self.env['csrd.esrs'].search([
            ('category_id', '=', category_id.id),
            ('financial_materiality', '!=', False),
            ('impact_materiality', '!=', False)
        ])

        if csrd_esrs_ids:
            csrd_esrs_data = []
            for csrd_esrs_id in csrd_esrs_ids:
                # Convert to float values
                financial_val = int(csrd_esrs_id.financial_materiality) / 10
                impact_val = int(csrd_esrs_id.impact_materiality) / 10

                # Handle edge case of 1.0 values - adjust to 0.99 to prevent rendering issues
                if financial_val >= 1.0:
                    financial_val = 0.99
                if impact_val >= 1.0:
                    impact_val = 0.99

                csrd_esrs_data.append(
                    f"{csrd_esrs_id.csrd_id.replace('.', '-').replace(':', '')}: [{financial_val}, {impact_val}]"
                )
        else:
            csrd_esrs_data = False
        return csrd_esrs_data

    def _quadrant_chart(self, data):
        if not data:
            data = ""
        quadrant_chart = f"""
            quadrantChart
                title Dubbel väsentlighetsanalys enligt CSRD
                x-axis "Låg finansiell väsentlighet"--> "Hög finansiell väsentlighet"
                y-axis "Låg påverkansväsentlighet"--> "Hög påverkansväsentlighet"
                quadrant-1 "Hög prioritet"
                quadrant-2 "Fokus på finansiell påverkan"
                quadrant-3 "Låg prioritet"
                quadrant-4 "Fokus på miljöpåverkan"
                {data}
        """
        return quadrant_chart

    def _get_swot_diagram(self):
        for rec in self:
            sub_category_ids = self.search([("parent_id", "child_of", rec.id), ("id", "!=", rec.id)])

            data = False
            if sub_category_ids:
                categories_data = []
                for sub_category in sub_category_ids.filtered(lambda x: x.parent_id):
                    if not sub_category.financial_materiality or not sub_category.impact_materiality:
                        continue

                    # Convert to float values
                    fin_val = int(sub_category.financial_materiality) / 10
                    imp_val = int(sub_category.impact_materiality) / 10

                    # Handle edge case of 1.0 values
                    if fin_val >= 1.0:
                        fin_val = 0.99
                    if imp_val >= 1.0:
                        imp_val = 0.99

                    categories_data.append(
                        f"{sub_category.name.replace(':', '')}: [{fin_val}, {imp_val}]"
                    )

                data = '\n'.join(categories_data) if categories_data else False
            else:
                if csrd_esrs_data := self._get_csrd_category_lines(rec):
                    csrd_esrs = '\n'.join(csrd_esrs_data)
                    data = csrd_esrs
            rec.swot_diagram = self._quadrant_chart(data=data)

    swot_diagram = fields.Text(string='SWOT Diagram', compute=_get_swot_diagram)