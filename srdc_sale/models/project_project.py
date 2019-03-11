# -*-coding: utf-8 -*-
from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    full_name = fields.Char()
    street = fields.Char()
    district_id = fields.Many2one('res.country.district')
    ward_id = fields.Many2one('res.country.ward')
    state_id = fields.Many2one('res.country.state', default=lambda self: self.env.ref('l10n_vn.state_vn_VN-SG'))
    country_id = fields.Many2one('res.country', default=lambda self: self.env.ref('base.vn'))
    location_x = fields.Float(string='Location x', digit=(16, 7))
    location_y = fields.Float(string='Location y', digit=(16, 7))
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('close', 'Close')
    ], default='new')
    # total_volume = fields.Float(string='Total Volume', compute='_compute_total_volume', store=True)
    rdc_volume = fields.Float(string='RDC Estimate Volume')
    customer_ids = fields.One2many('project.customer', 'project_id', string='Customer')
    competitor_ids = fields.One2many('project.competitor', 'project_id', string='Competitor')
    order_count = fields.Integer(compute='_compute_order_count')
    distance_ids = fields.One2many('project.distance', 'project_id', string='Distances')
    code = fields.Char()
    description = fields.Text()
    consultant_id = fields.Many2one('res.partner', 'Consultant', domain="[('consultant','=',1)]")
    consultant_chief_id = fields.Many2one('res.partner', 'Chief Consultant')
    consultant_other_id = fields.Many2one('res.partner', 'Other Contact')
    partner_id = fields.Many2one('res.partner', 'Investor', domain="[('investor','=',1)]")
    partner_manager_id = fields.Many2one('res.partner', 'Project Manager')
    partner_other_id = fields.Many2one('res.partner', 'Other Contact')
    actual_supplied = fields.Float('Competitor Actual Supplied', readonly=True)
    input_ids = fields.One2many('project.project.input', 'project_id')
    estimate_start = fields.Date()
    estimate_end_date = fields.Date()
    project_report_ids = fields.One2many('project.report', 'project_id')

    def _compute_order_count(self):
        for rec in self:
            rec.order_count = self.env['sale.order'].search_count([('project_id', '=', rec.id)])

    # @api.depends('input_ids.estimate_volume')
    # def _compute_total_volume(self):
    #     for rec in self:
    #         rec.total_volume = sum(rec.input_ids.mapped('estimate_volume'))


