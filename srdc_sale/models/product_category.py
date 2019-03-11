# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ProductTeamplate(models.Model):
    _inherit = 'product.category'

    sequence = fields.Integer()
