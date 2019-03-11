# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcPurchaseAttributeValue(models.Model):
    _name = 'srdc.purchase.attribute.value'

    name = fields.Char()
    attribute_id = fields.Many2one('srdc.purchase.attribute', string='Attribute')
