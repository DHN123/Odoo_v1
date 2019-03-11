# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcTrialmixResult(models.Model):
    _name = 'srdc.trialmix.result'

    value_id = fields.Many2one('srdc.trialmix.result.value')
    value = fields.Integer()
    line_id = fields.Many2one('srdc.trialmix.line')
