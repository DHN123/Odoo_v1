# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcPurchaseOderLine(models.Model):
    _name = 'srdc.purchase.order.line'

    # def _get_default_uom(self):
    #     uom_default = self.env['srdc.uom.uom'].search([('name', 'ilike', 'Cái')])
    #     if uom_default:
    #         return uom_default.id
    #     return super(SrdcPurchaseOderLine, self).get_default_uom()

    name = fields.Char(string='Product')
    description = fields.Char()
    product_qty = fields.Integer()
    srdc_product_uom_id = fields.Many2one('srdc.uom.uom')
    approx_unit_price = fields.Float()
    actual_price = fields.Float(string='Actual Price', compute='_compute_actual_price')
    vat_id = fields.Many2one('srdc.vat', string='VAT(%)')
    grand_total = fields.Float(string='Grand Total', compute='_compute_grand_total')
    srdc_purchase_order_id = fields.Many2one('srdc.purchase.order', string='Product')

    @api.onchange('product_qty', 'approx_unit_price')
    def _compute_actual_price(self):
        for rec in self:
            if rec.product_qty and rec.approx_unit_price:
                rec.actual_price = rec.product_qty * rec.approx_unit_price

    @api.onchange('product_qty', 'approx_unit_price', 'vat_id')
    def _compute_grand_total(self):
        for rec in self:
            if rec.actual_price and rec.vat_id:
                rec.grand_total = rec.actual_price + (rec.vat_id.id * 0.1 * rec.actual_price)
            else:
                rec.grand_total = rec.actual_price
