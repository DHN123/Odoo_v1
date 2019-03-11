from odoo import api, fields, models


class WizardRequestQC(models.TransientModel):
    _name = 'wizard.request.qc'

    choose_type = fields.Selection([
        ('deli', 'Delivery Mix Code'),
        ('batch', 'P & L Mix Code'),
        ('both', 'Delivery & P and L Mix Code'),
    ], default='deli')

    @api.multi
    def request_to_qc(self):
        order = self.env['sale.order'].browse(self._context.get('active_id'))
        procedures = self.env['srdc.mix.procedure'].search([
            ('order_id', '=', order.id),
            ('choose_type', '=', 'batch'),
        ])
        sale_commission_rate = self.env['ir.config_parameter'].sudo().get_param('sale_commission_rate', 0.75)
        if (self.choose_type == 'batch' and (not order.is_refund or not procedures)) or self.choose_type == 'deli' or self.choose_type == 'both':
            data = {
                'order_id': order.id,
                'partner_id': order.partner_id.id,
                'project_id': order.project_id.id,
                'state': 'draft',
                'transportation_fee': order.transportation,
                'toll_booths_num': order.toll_booths_num,
                'is_rush_hour': order.is_rush_hour,
                'commission': order.commission / float(sale_commission_rate),
                'traffic_police_fee': self.env.user.company_id.traffic_police,
                'testing_fee': self.env.user.company_id.testing_fee,
                'other_cost': self.env.user.company_id.other_cost,
                'deadline': order.deadline,
                'choose_type': self.choose_type,
                'line_ids': [],
            }
            for line in order.order_line:
                data['line_ids'].append((0, 0, {
                    'product_id': line.product_id.id,
                    'line_id': line.id,
                }))
            self.env['srdc.mix.procedure'].create(data)
        else:
            procedures.write({
                'is_refund': True,
                'state': 'draft',
            })
        if self.choose_type != 'deli':
            order.state = 'qc_optimize'
