# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcHrConfiguration(models.Model):
    _name = 'srdc.hr.employees.status'

    name = fields.Char()
    symbol = fields.Char()
    type_of_labor_contract = fields.Char()
