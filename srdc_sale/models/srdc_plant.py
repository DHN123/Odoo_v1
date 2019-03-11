# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SRDCPlant(models.Model):
    _name = 'srdc.plant'

    code = fields.Char()
    location_x = fields.Float('Location X', digits=(16, 7))
    location_y = fields.Float('Location Y', digits=(16, 7))
