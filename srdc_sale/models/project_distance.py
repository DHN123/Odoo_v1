from odoo import api, fields, models


class ProjectDistance(models.Model):
    _name = "project.distance"

    project_id = fields.Many2one('project.project')
    distance = fields.Float()
    company_id = fields.Many2one('res.company')
