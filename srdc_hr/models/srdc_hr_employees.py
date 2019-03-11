# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcHr(models.Model):
    _inherit = 'hr.employee'

    capitalization_name = fields.Char()
    msnv = fields.Integer()
    department_code_id = fields.Many2one('hr.department', string='Department Code')
    day_of_job = fields.Datetime()
    status_id = fields.Many2one('srdc.hr.employees.status')










