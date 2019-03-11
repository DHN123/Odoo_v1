# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ResCountryWard(models.Model):
    _name = 'res.country.ward'

    name = fields.Char()
    district_id = fields.Many2one('res.country.district')
