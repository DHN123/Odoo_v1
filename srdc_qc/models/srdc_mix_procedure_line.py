from odoo import api, fields, models


class SRDCMixProcedureLine(models.Model):
    _name = "srdc.mix.procedure.line"
    _description = "Mix Procedure.line"

    procedure_id = fields.Many2one('srdc.mix.procedure')
    product_id = fields.Many2one('product.product')
    mix_design_id = fields.Many2one('srdc.mix.design', 'Mix P & L Code')
    mix_design_2nd_id = fields.Many2one('srdc.mix.design', 'Mix DELI Code')
    line_id = fields.Many2one('sale.order.line')
    total_amount = fields.Float(string='Raw material')
    other_variable = fields.Float(related='procedure_id.other_variable')
    currency_id = fields.Many2one('res.currency', related='procedure_id.currency_id', readonly=True)

    @api.onchange('mix_design_id', 'procedure_id.is_refund')
    def set_mix_design_id(self):
        for rec in self:
            if rec.procedure_id.is_refund:
                rec.total_amount = rec.mix_design_id.optimize_total_amount
            else:
                rec.total_amount = rec.mix_design_id.total_amount
