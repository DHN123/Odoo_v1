from odoo import api, fields, models


class SRDCIO(models.Model):
    _name = "srdc.io"

    name = fields.Char()
    contract_id = fields.Many2one('srdc.contract')
    distance = fields.Float(compute='_computing_distance')
    line_ids = fields.One2many('srdc.io.line', 'io_id')
    file_name = fields.Char()
    data_file = fields.Binary('Data File')
    is_temp = fields.Boolean('Temporary??')
    sampling_standard = fields.Text()
    description = fields.Text()
    type_standard = fields.Selection([
        ('bs', 'BS'),
        ('aci', 'ACI'),
        ('tcvn', 'TCVN'),
    ], string='Standard', default='tcvn')
    company_id = fields.Many2one('res.company')

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.contract_id.name or '', rec.company_id.name or '')))
        return res

    @api.onchange('company_id', 'contract_id', 'contract_id.project_id')
    def _computing_distance(self):
        for rec in self:
            rec.distance = sum(
                rec.contract_id.project_id.distance_ids.filtered(
                    lambda d: d.company_id == rec.company_id).mapped('distance'))
