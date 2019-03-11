# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ConcretePumpAttrCategory(models.Model):
    _name = 'srdc.concrete.pump.volume'

    name = fields.Float(string="Value")
