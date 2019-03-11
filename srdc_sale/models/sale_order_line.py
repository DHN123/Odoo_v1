from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    computed_price = fields.Float('Variable costs')
    margin = fields.Float('Contribution Margin', compute="_compute_margin")
    mix_code_id = fields.Many2one('srdc.mix.design', 'Mix Code P&L')
    mix_code_deli_id = fields.Many2one('srdc.mix.design', 'Mix Code Deli')

    @api.onchange('price_unit', 'computed_price')
    def _compute_margin(self):
        for rec in self:
            rec.margin = rec.price_unit * 10 / 11 - rec.computed_price
