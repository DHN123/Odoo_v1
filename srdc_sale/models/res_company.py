from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'

    district_id = fields.Many2one('res.country.district')
    ward_id = fields.Many2one('res.country.ward')
    location_x = fields.Float(string='Location x', digit=(16, 7))
    location_y = fields.Float(string='Location y', digit=(16, 7))
    code = fields.Char()
