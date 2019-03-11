# -*-coding: utf-8 -*-
from odoo import api, fields, models, _

class SrdcVat(models.Model):
    _name = 'srdc.vat'

    name = fields.Float()
