from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SRDCMixProcedure(models.Model):
    _name = "srdc.mix.procedure"
    _description = "Mix Procedure"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    order_id = fields.Many2one('sale.order', 'Customer Order')
    partner_id = fields.Many2one('res.partner', 'Customer')
    project_id = fields.Many2one('project.project', 'Project')
    description = fields.Text()
    line_ids = fields.One2many('srdc.mix.procedure.line', 'procedure_id')
    request_date = fields.Date('Request Date', default=fields.Date.context_today)
    choose_type = fields.Selection([
        ('deli', 'Delivery Mix Code'),
        ('batch', 'P & L Mix Code'),
        ('both', 'Delivery & P and L Mix Code'),
    ], default='deli', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done_optimize', 'Finish Optimize'),
        ('qc_approved', 'Compute Price'),
        ('done', 'Done'),
        ('pending', 'Pending'),
        ('cancel', 'Cancel'),
    ], default='draft', track_visibility='onchange')
    transportation_fee = fields.Float('Transportation')
    traffic_police_fee = fields.Float(
        'Traffic Police', default=lambda self: self.env.user.company_id.traffic_police)
    ice_water_fee = fields.Float('Ice Water')
    toll_booths_num = fields.Integer('Toll Booths Num.', readonly=True)
    toll_fee = fields.Float()
    is_rush_hour = fields.Boolean('Rush hour?', readonly=True)
    rush_hour_fee = fields.Float()
    testing_fee = fields.Float(default=lambda self: self.env.user.company_id.testing_fee)
    other_cost = fields.Float('Others variable cost', default=lambda self: self.env.user.company_id.other_cost)
    commission = fields.Float()
    other_variable = fields.Float(compute='_compute_other_variable', store=True)
    is_refund = fields.Boolean(default=False)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    @api.multi
    @api.depends(
        'transportation_fee',
        'traffic_police_fee',
        'ice_water_fee',
        'toll_fee',
        'rush_hour_fee',
        'testing_fee',
        'other_cost',
        'commission')
    def _compute_other_variable(self):
        for rec in self:
            rec.other_variable = rec.transportation_fee + rec.traffic_police_fee + rec.ice_water_fee + \
                                 rec.toll_fee + rec.rush_hour_fee + rec.testing_fee + rec.other_cost + rec.commission

    @api.multi
    def name_get(self):
        return [(procedure.id, procedure.order_id.name) for procedure in self]

    @api.multi
    def btn_start_optimize(self):
        self.write({'state': 'in_progress'})

    @api.multi
    def btn_qc_approve(self):
        for rec in self:
            if rec.choose_type in ['batch', 'both']:
                rec.order_id.action_request_to_accounting()
                rec.write({'state': 'qc_approved'})
            if rec.choose_type == 'deli':
                rec.write({'state': 'done'})

    @api.multi
    def btn_done_optimize(self):
        for rec in self:
            if rec.choose_type == 'both':
                if len(rec.line_ids) != len(rec.line_ids.filtered(lambda l: l.mix_design_id)) or \
                   len(rec.line_ids) != len(rec.line_ids.filtered(lambda l: l.mix_design_2nd_id)):
                    raise UserError(_('You need to add all Mix Design to the Grade!'))
                rec.write({'state': 'done_optimize'})
            elif rec.choose_type == 'batch':
                if len(rec.line_ids) != len(rec.line_ids.filtered(lambda l: l.mix_design_id)):
                    raise UserError(_('You need to add all Mix Design to the Grade!'))
                rec.write({'state': 'done_optimize'})
            else:
                if len(rec.line_ids) != len(rec.line_ids.filtered(lambda l: l.mix_design_2nd_id)):
                    raise UserError(_('You need to add all Mix Design to the Grade!'))
                rec.write({'state': 'done'})

    @api.multi
    def btn_approve(self):
        self.write({'state': 'done'})
        for rec in self:
            for line in rec.line_ids:
                line.line_id.write({
                    'mix_code': line.mix_design_id.name,
                    'computed_price': line.mix_design_id.total_amount + rec.other_variable
                })
            rec.order_id.action_request_to_sale()

    @api.multi
    def btn_pending(self):
        self.write({'state': 'pending'})

    @api.multi
    def btn_set_to_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def btn_cancel(self):
        self.write({'state': 'cancel'})
