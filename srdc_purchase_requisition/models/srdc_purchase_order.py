# -*-coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime


class SrdcPurchaseOrder(models.Model):
    _name = 'srdc.purchase.order'

    name = fields.Char(string='Order Number')
    pr_number = fields.Integer(string="PR Number", store=True)
    # requestor_id = fields.Many2one('hr.employee', string="Requestor", required=True)
    # department_id = fields.Many2one('hr.department', stirng="Department", required=True)
    to = fields.Char(string="To")
    quotation_filename = fields.Char(string="Quotation")
    quotation_file = fields.Binary()
    date_order = fields.Datetime(default=datetime.today(), required=True, string='Order Date')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    state = fields.Selection([
        ('new', _('Requestor')),
        ('verify', _('Verified By')),
        ('to_manager_of_department_approve', _('To Manager of Department Approve')),
        ('purchasing', _('To Manager of Purchasing Approve')),
        ('to_manager_of_purchasing_approve', _('To Manager of Purchasing Approve')),
        ('to_finance_approve', _('To Finance Approve')),
        ('to_dgd_approve', _('To DGD/GD Approve')),
        ('done', _('Done')),
        ('cancel', _('Cancel')),
        ('pending', _('Pending'))
    ], default='new')
    srdc_purchase_order_line_ids = fields.One2many('srdc.purchase.order.line', 'srdc_purchase_order_id', string='Srdc Purchase Order Line')
    attribute_line_ids = fields.One2many('srdc.purchase.attribute.line', 'purchase_order_id', string='Attribute Line')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('srdc.purchase.order') or _('New')
            return super(SrdcPurchaseOrder, self).create(vals)

    # @api.onchange('department_id')
    # def filter_vendor_id(self):
    #     for rec in self:
    #         if rec.department_id:
    #             vendor_ids = self.env['res.partner'].search([
    #                 ('department_id', '=', rec.department_id.id),
    #                 ('supplier', '=', True)
    #             ])
    #             print(vendor_ids)
    #             return {'domain': {'vendor_id': [('id', 'in', vendor_ids.ids)]}}
    #         else:
    #             return {'domain': {'vendor_id': []}}
    #
    # @api.onchange('department_id')
    # def filter_requestor_id(self):
    #     for rec in self:
    #         if rec.department_id:
    #             requestor_ids = self.env['hr.employee'].search([
    #                 ('department_id', '=', rec.department_id.id),
    #             ])
    #             return {'domain': {'requestor_id': [('id', 'in', requestor_ids.ids)]}}
    #         else:
    #             return {'domain': {'requestor_id': []}}
    #
    # @api.onchange('requestor_id')
    # def pr_auto_number_(self):
    #     for rec in self:
    #         dem = self.env['srdc.purchase.order'].search([]).mapped('pr_number')
    #         if len(dem) == 0:
    #             rec.pr_number = 1
    #         else:
    #             rec.pr_number = max(dem) + 1

    def action_request_to_verify(self):
        self.write({'state': 'verify'})

    def action_request_to_manager_of_department(self):
        self.write({'state': 'to_manager_of_department_approve'})

    def action_request_purchasing(self):
        self.write({'state': 'purchasing'})

    def action_request_to_manager_of_purchasing(self):
        self.write({'state': 'to_manager_of_purchasing_approve'})

    def action_request_to_fiance(self):
        self.write({'state': 'to_finance_approve'})

    def action_request_to_dgd(self):
        self.write({'state': 'to_dgd_approve'})

    def action_request_to_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_reset(self):
        self.write({'state': 'new'})

    def action_pending(self):
        self.write({'state': 'pending'})
