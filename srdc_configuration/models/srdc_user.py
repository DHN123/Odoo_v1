# -*-coding: utf-8 -*-
from odoo import api, fields, models, _


class SrdcUser(models.Model):
    _inherit = 'res.users'

    # def _get_departments(self):
    #     departments = self.env['hr.department'].search([]).mapped('name')
    #     return super(SrdcUser, self)._get_departments()

    # department_ids = fields.Many2many(
    #     'hr.department', string='Allowed Department',
    #     domain=lambda self: self.env['hr.department'].search([]).mapped('name')
    # )
    # current_department_id = fields.Many2one('hr.department', string='Current Company')
