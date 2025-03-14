from odoo import api, fields, models, tools, _


class CsrdESRS(models.Model):
    _inherit = "csrd.esrs"

    model_id = fields.Many2one(
        'ir.model', string='Recipients Model',
        ondelete='cascade', required=True,
    )
    model = fields.Char(
        string='Model', compute='_compute_model')

    domain = fields.Char('Domain')
    model_name = fields.Char(
        string='Model Name',
        related='model_id.model', readonly=True, related_sudo=True)

    @api.depends('model_id')
    def _compute_model(self):
        for mailing in self:
            mailing.model = mailing.model_id.model

    def _split_batch(self):
        batch_size = 500
        for sms_batch in tools.split_every(batch_size, self.search([('model_id', '!=', False)]).ids):
            yield sms_batch

    def _cron_check_csrd_data_point(self):
        for batch_ids in self._split_batch():
            rec_ids = self.browse(batch_ids)
            for rec_id in rec_ids:
                if rec_id.domain:
                    count = self.env[rec_id.model].search_count(eval(rec_id.domain))
                    self._esrs_line(rec_id, count)

    def _esrs_line(self, csrd_id, count):
        csrd_esrs_id = self.env['esrs.line'].search([('csrd_esrs_id', '=', csrd_id.id)], limit=1)
        if csrd_esrs_id:
            csrd_esrs_id.write({'quantity': count})
        else:
            self.env['esrs.line'].create({'csrd_esrs_id': csrd_id.id, 'quantity': count})
