# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ProjectReport(models.Model):
    _name = 'project.report'

    description = fields.Html()
    project_id = fields.Many2one('project.project')
