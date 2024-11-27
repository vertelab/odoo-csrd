from odoo import models, fields, api

class CSRDESRS(models.Model):
    _name = 'csrd.esrs'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Creates ESRS datapoints'
    _rec_name = "csrd_name"

    # name = fields.Char(compute='_compute_name', store=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        help="If set, page is accessible only from this company",
        index=True,
        ondelete="cascade",
        default=lambda self: self.env.company,
    )

    survey_id = fields.Many2one(comodel_name='survey.survey')

    active = fields.Boolean(default=True)

    document_page_manual_ids = fields.One2many(comodel_name="document.page.csrd.esrs", inverse_name="csrd_esrs_id")

    currency_id = fields.Many2one('res.currency', string="Currency",
                                 related='company_id.currency_id')

    stage = fields.Selection(selection=[
       ('draft', 'Draft'),
       ('done', 'Done'),
    ], string='Status', required=True, copy=False,
    tracking=True, default='draft')

    description = fields.Html(string="Description")
    estimated_value = fields.Float(string="Estimated Value")

    category_id = fields.Many2one(comodel_name="csrd.esrs.category", string="ESRS Category", compute="_compute_category_id", store=True)

    csrd_sheet_name = fields.Selection(
            selection=[
            ('ESRS 2','ESRS 2'),
            ('ESRS 2 MDR','ESRS 2 MDR'),
            ('ESRS E1','ESRS E1'),
            ('ESRS E2','ESRS E2'),
            ('ESRS E3','ESRS E3'),
            ('ESRS E4','ESRS E4'),
            ('ESRS E5','ESRS E5'),
            ('ESRS S1','ESRS S1'),
            ('ESRS S2','ESRS S2'),
            ('ESRS S3','ESRS S3'),
            ('ESRS S4','ESRS S4'),
            ('ESRS G1','ESRS G1'),
            ], 
            default=None)

    csrd_id = fields.Char(string="ID")
    csrd_esrs = fields.Char(string="ESRS")
    csrd_dr = fields.Char(string="Disclosure Requirement")
    csrd_paragraph = fields.Char(string="Paragraph")
    csrd_related_ar = fields.Char(string="Related_AR")
    csrd_name = fields.Char(string="Name", translate=True)
    csrd_data_type = fields.Char(string="Data Type")
    csrd_conditional_or_alternative_dp = fields.Char(string="Conditional or Alternative DP")
    csrd_may_v = fields.Char(string="May V")
    csrd_appendix_b = fields.Char(string="Appendix B")
    csrd_appendix_c_less_then_750 = fields.Char(string="Appendix C < 750")
    csrd_appendix_c_more_then_750 = fields.Char(string="Appendix C > 750")

    @api.depends("csrd_sheet_name")
    def _compute_category_id(self):
        for rec in self:
            category_id = self.env["csrd.esrs.category"].search([("name", '=', rec.csrd_sheet_name)])
            if category_id:
                rec.category_id = category_id

