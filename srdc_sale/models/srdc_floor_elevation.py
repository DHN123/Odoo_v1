from odoo import api, fields, models


class FloorElevation(models.Model):
    _name = 'srdc.floor.elevation'

    name = fields.Char()
