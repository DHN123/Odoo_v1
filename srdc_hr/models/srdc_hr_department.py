# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcHrDepartment(models.Model):
    _inherit = 'hr.department'

    department_code = fields.Char()
    functions_of_each_plant = fields.Char()
