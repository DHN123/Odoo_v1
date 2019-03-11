# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcPurchaseAttribute(models.Model):
    _name = 'srdc.purchase.attribute'
    _inherit = 'product.attribute'


class SrdcPurchaseTemplateAttribute(models.Model):

    _name = 'srdc.purchase.attribute.line'

    purchase_order_id = fields.Many2one('srdc.purchase.order', string='Purchase Order')
    attribute_id = fields.Many2one('srdc.purchase.attribute', string='Attribute')
    value_ids = fields.Many2many('srdc.purchase.attribute.value', string='Value')

    def check_create_attribute(self):
        for rec in self:
            if rec.attribute_id:
                rec.value_ids = self.env['srdc.purchase.attribute.value'].search([
                    ('attribute_id', 'in', rec.attribute_id.mapped('name'))
                ])
