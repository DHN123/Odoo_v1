#-*-coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    source = fields.Char()
    optimize_price = fields.Float()

    @api.multi
    def name_get(self):
        return [(si.id, "%s - %s" % (si.name.name, si.product_name)) for si in self]
