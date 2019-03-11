# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcUom(models.Model):
    _name = 'srdc.uom.uom'
    _order =  'name'

    name = fields.Char()
    active = fields.Boolean()
