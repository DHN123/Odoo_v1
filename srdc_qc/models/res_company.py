from odoo import api, fields, models


class Company(models.Model):
    _inherit = 'res.company'

    traffic_police = fields.Integer()
    testing_fee = fields.Integer()
    other_cost = fields.Float('Others variable cost')
