# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ProjectProjectInput(models.Model):
    _name = 'project.project.input'

    name = fields.Char()
    estimate_volume = fields.Float()
    note = fields.Char()
    project_id = fields.Many2one('project.project')
