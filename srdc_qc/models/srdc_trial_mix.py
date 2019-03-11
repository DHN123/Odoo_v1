# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcTrialMix(models.Model):
    _name = 'srdc.trialmix'

    name = fields.Char()
    order_id = fields.Many2one('sale.order')
    plan_date = fields.Date()
    line_ids = fields.One2many('srdc.trialmix.line', 'trialmix_id', 'Line')
    state = fields.Selection([
        ('draft', _('Draft')),
        ('committed', _('SM Approved')),
        ('approved', _('PS Confirmed')),
        ('approved_qc', _('QC Approved')),
        ('done', _('Done')),
        ('close', _('Close'))
    ], default='draft')
    user_id = fields.Many2one('res.users', 'Assign to', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', 'Plant', domain="[('parent_id', '!=', False)]")
    minutes_of_trialmix_filename = fields.Char('Minutes of TrialMix Filename')
    minutes_of_trialmix_file = fields.Binary('Minutes of TrialMix')
    material_sampling_filename = fields.Char('Material Sampling Filename')
    material_sampling_file = fields.Binary('Material Sampling')

    @api.multi
    def btn_commit_action(self):
        self.write({'state': 'committed'})

    @api.multi
    def btn_approve_action(self):
        self.write({'state': 'approved'})

    @api.multi
    def btn_approve_qc_action(self):
        self.write({'state': 'approved_qc'})

    @api.multi
    def btn_close_action(self):
        self.write({'state': 'close'})

    @api.multi
    def btn_done_action(self):
        for rec in self:
            for line in rec.line_ids.filtered(lambda l: l.order_line_id and l.mix_code):
                line = self.env['sale.order.line'].browse(line.order_line_id)
                line.write({'mix_code': line.mix_code})
        self.write({'state': 'done'})

    @api.multi
    def btn_set_to_draft(self):
        self.write({'state': 'draft'})
