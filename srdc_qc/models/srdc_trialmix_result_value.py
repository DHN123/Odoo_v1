# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcTrialmixResultValue(models.Model):
    _name = 'srdc.trialmix.result.value'

    name = fields.Char()
    sequence = fields.Integer()
