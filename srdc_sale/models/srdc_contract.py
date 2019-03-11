# -*-coding: utf-8 -*-
from odoo import api, fields, models


class SrdcContract(models.Model):
    _name = 'srdc.contract'
    _description = 'SRDC Sale Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)
    date_from = fields.Date(default=fields.Date.context_today)
    date_to = fields.Date()
    date_plan_to = fields.Date('Target Deadline')
    payment_date = fields.Date()
    description = fields.Text()
    max_qty = fields.Float()
    max_amount = fields.Float()
    is_temp = fields.Boolean()
    is_sign = fields.Boolean()
    user_id = fields.Many2one('res.users', string='Assign To', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('lawyer', 'Lawyer'),
        ('committed', 'Committed'),
        ('done', 'Done'),
        ('pending', 'Pending'),
        ('cancel', 'Cancel')
    ], default='draft')
    order_count = fields.Integer(compute='_compute_order_count')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term')
    # line_ids = fields.One2many('srdc.contract.line', 'contract_id')
    count_io = fields.Integer(compute='_count_io')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    def _count_io(self):
        for rec in self:
            rec.count_io = self.env['srdc.io'].search_count([('contract_id', '=', rec.id)])

    def _compute_order_count(self):
        for rec in self:
            rec.order_count = self.env['sale.order'].search_count([('contract_id', '=', rec.id)])

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            project_customer_ids = self.env['project.customer'].search([
                ('partner_id', '=', self.partner_id.id)
            ])
            return {'domain': {'project_id': [('id', 'in', project_customer_ids.mapped('project_id').ids)]}}
        else:
            return {'domain': {'project_id': []}}

    @api.multi
    def btn_committed(self):
        self.write({'state': 'committed'})

    @api.multi
    def btn_done(self):
        self.write({'state': 'done'})

    @api.multi
    def btn_set_to_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def btn_pending(self):
        self.write({'state': 'pending'})

    @api.multi
    def btn_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def btn_lawyer(self):
        self.write({'state': 'lawyer'})

    @api.multi
    def btn_lawyer_approve(self):
        self.write({'state': 'draft'})
