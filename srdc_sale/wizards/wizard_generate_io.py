from odoo import api, fields, models, _


class WizardGenerateIO(models.Model):
    _name = 'wizard.generate.io'

    @api.multi
    def _get_io(self):
        active_id = self._context.get('active_id')
        order = self.env['sale.order'].browse(active_id)
        return [('contract_id', '=', order.contract_id.id)]

    name = fields.Char()
    is_temp = fields.Boolean('Temporary ??')
    io_id = fields.Many2one('srdc.io', 'Internal Order', domain=_get_io)

    @api.multi
    def btn_generate_io(self):
        active_id = self._context.get('active_id')
        active_model = self._context.get('active_model')
        order = self.env[active_model].browse(active_id)
        if self.io_id:
            io = self.io_id
            io.write({
                'line_ids': [(0, 0, {
                    'product_id': l.product_id.id,
                    'mix_code': l.mix_code_deli,
                    'amount': l.price_unit,
                    'quantity': l.product_uom_qty,
                    'is_temp': self.is_temp,
                }) for l in order.order_line]
            })
        else:
            io = self.env['srdc.io'].create({
                'name': self.name,
                'is_temp': self.is_temp,
                'contract_id': order.contract_id.id,
                'line_ids': [(0, 0, {
                    'product_id': l.product_id.id,
                    'mix_code': l.mix_code_deli,
                    'amount': l.price_unit,
                    'quantity': l.product_uom_qty,
                    'is_temp': self.is_temp,
                }) for l in order.order_line]
            })
        order.write({'io_id': io.id})
        return {
            'name': _('Internal Order'),
            'res_model': 'srdc.io',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': io.id,
        }
