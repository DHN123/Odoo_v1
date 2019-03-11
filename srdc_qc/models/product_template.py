from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    optimize_price = fields.Float()
    source = fields.Char()
