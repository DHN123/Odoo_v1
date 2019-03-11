# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcTrialMix(models.Model):
    _name = 'srdc.trialmix.line'

    order_line_id = fields.Many2one('sale.order.line')
    product_id = fields.Many2one('product.product', related='order_line_id.product_id')
    mix_id = fields.Many2one('srdc.mix.design', 'Mix Design')
    trialmix_id = fields.Many2one('srdc.trialmix', string='Trial Mix')
    price = fields.Float()
    type = fields.Selection([
        ('cube', _('Cube')),
        ('cylindrical', _('Cylindrical'))
    ], default='cube')
    deli_mix_design_filename = fields.Char('DELI Mix-Design Name')
    deli_mix_design_file = fields.Binary('DELI Mix-Design')
    tech_batch_report_filename = fields.Char('Tech Batch Report Name')
    tech_batch_report_file = fields.Binary('Tech Batch Report')
    delivery_note_filename = fields.Char('Delivery Note Name')
    delivery_note_file = fields.Binary('Delivery Note')
    result_ids = fields.One2many('srdc.trialmix.result', 'line_id')
    note = fields.Text()

    @api.model
    def default_get(self, fields):
        rec = super(SrdcTrialMix, self).default_get(fields)
        values = self.env['srdc.trialmix.result.value'].search([])
        rec['result_ids'] = [(0, 0, {'value_id': v.id}) for v in values]
        return rec
