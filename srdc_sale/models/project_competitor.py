# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ProjectCompetitor(models.Model):
    _name = 'project.competitor'

    project_id = fields.Many2one('project.project', string='Project')
    partner_id = fields.Many2one(
        'res.partner', string='Partner', domain="[('is_competitor','=',1), ('parent_id', '=', False)]")
    description = fields.Char()
