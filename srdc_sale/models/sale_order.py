# -*-coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project', 'Project')
    contract_id = fields.Many2one('srdc.contract', 'Contract')
    state = fields.Selection([
        ('new', _('Draft')),
        ('qc_optimize', _('Optimize Mix Design')),
        ('compute_price', _('Compute Price')),
        ('to_sale_approve', _('To Sale Approve')),
        ('to_manager_approve', _('To Manager Approve')),
        ('draft', _('Quotation')),
        ('sent', _('Quotation Sent')),
        ('sale', _('Sales Order')),
        ('done', _('Locked')),
        ('cancel', _('Cancelled')),
    ], default='new')
    transportation = fields.Float()
    toll_booths_num = fields.Float('Toll Booths Num.')
    is_rush_hour = fields.Boolean('Rush hour?')
    commission = fields.Float()
    deadline = fields.Date()
    is_refund = fields.Boolean()
    is_fast_quotation = fields.Boolean()
    io_id = fields.Many2one('srdc.io', 'Internal Order')
    trial_mix_count = fields.Integer(compute='compute_trial_mix_count')
    procedure_count = fields.Integer(compute='compute_procedure_count')
    concrete_pump_ids = fields.One2many('srdc.concrete.pump.category', 'sale_order_id', string='Concrete Pump')
    order_pump_sale = fields.Many2one('srdc.concrete.pump.volume', string='Oder Pump')

    @api.onchange('order_pump_sale')
    def get_data_from_accounting(self):
        for rec in self:
            if rec.order_pump_sale:
                list_data = []
                data = self.env['srdc.concrete.pump.category'].search([
                    ('sale_order_id', '=', False),
                    ('order_pump', '=', rec.order_pump_sale.id)])
                for d in data:
                    list_data.append(
                        (0, 0, {
                            'name': d.name,
                            'floor_elevation': d.floor_elevation,
                            'order_pump': d.order_pump,
                            'block_m3_nail': d.block_m3_nail,
                            'block_m3_component': d.block_m3_component,
                            'block_times_nail': d.block_times_nail,
                            'block_times_component': d.block_times_component,
                            'selection': d.selection
                        })
                    )
                rec.concrete_pump_ids = list_data
            else:
                rec.concrete_pump_ids = ''

    def compute_trial_mix_count(self):
        for rec in self:
            rec.trial_mix_count = self.env['srdc.trialmix'].search_count([('order_id', '=', rec.id)])

    def compute_procedure_count(self):
        for rec in self:
            rec.procedure_count = self.env['srdc.mix.procedure'].search_count([('order_id', '=', rec.id)])

    @api.onchange('partner_id')
    def _check_customer(self):
        for rec in self:
            if rec.partner_id:
                rec.project_id = rec.project_id.customer_ids.filtered(lambda c: c.partner_id == rec.partner_id).mapped('project_id')

    @api.multi
    def action_request_to_accounting(self):
        self.write({'state': 'compute_price'})

    @api.multi
    def action_comeback_to_qc(self):
        procedures = self.env['srdc.mix.procedure'].search([
            ('origin', 'in', self.mapped('name')),
            ('choose_type', '=', 'batch'),
        ])
        procedures.write({
            'is_refund': True,
            'state': 'qc_approved',
        })
        self.write({
            'state': 'qc_optimize',
            'is_refund': True
        })

    @api.multi
    def action_request_to_sale(self):
        self.write({'state': 'to_sale_approve'})

    @api.multi
    def action_request_to_manager(self):
        self.write({'state': 'to_manager_approve'})

    @api.multi
    def action_request_to_quotation(self):
        self.state = 'draft'

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
    def btn_tender_quotation(self):
        sale_commission_rate = self.env['ir.config_parameter'].sudo().get_param('sale_commission_rate', 0.75)
        com = self.env.user.company_id
        for rec in self:
            # TODO: Compute toll free, rush hour??
            commission = rec.commission / float(sale_commission_rate)
            other_variable = rec.transportation + com.traffic_police + com.testing_fee + com.other_cost + commission
            for line in rec.order_line:
                mix_design = self.env['srdc.mix.design'].search([
                    ('product_id', '=', line.product_id.id),
                    ('is_standard', '=', True),
                ])
                if not mix_design:
                    mix_design = self.env['srdc.mix.design'].search([
                        ('product_id', '=', line.product_id.id),
                    ], order='sequence', limit=1)
                computed_price = mix_design.total_amount + other_variable
                line.write({
                    'mix_code': mix_design.id,
                    'computed_price': computed_price
                })
        self.write({
            'is_fast_quotation': True,
            'state': 'to_sale_approve'
        })
    #     return {
    #         'name': _('Mix Procedure'),
    #         'res_model': 'srdc.mix.procedure',
    #         'type': 'ir.actions.act_window',
    #         'context': {'search_default_origin': self.name},
    #         'view_mode': 'tree,form',
    #     }

    @api.multi
    def btn_request_trialmix(self):
        self.ensure_one()
        mix_obj = self.env['srdc.mix.design']
        trialmix_id = self.env['srdc.trialmix'].create({
            'order_id': self.id,
            'line_ids': [(0, 0, {
                'product_id': l.product_id.id,
                'mix_id': l.mix_code_id,
                'order_line_id': l.id
            }) for l in self.order_line]
        })
        return {
            'name': 'Trial Mix',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'srdc.trialmix',
            'res_id': trialmix_id.id
        }
