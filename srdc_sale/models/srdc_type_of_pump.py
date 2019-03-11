from odoo import api, fields, models


class TypeOfPump(models.Model):
    _name = 'srdc.type.of.pump'

    name = fields.Char()
