# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ResCountryDistrict(models.Model):
    _name = 'res.country.district'

    name = fields.Char()
    state_id = fields.Many2one('res.country.state', string='City')
