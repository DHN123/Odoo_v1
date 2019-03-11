from odoo import api, fields, models


class SRDCMixDesignLine(models.Model):
    _name = "srdc.mix.design.line"

    categ_id = fields.Many2one('product.category', srting='Product Category')
    mix_design_id = fields.Many2one('srdc.mix.design', string='Mix Design')
    product_id = fields.Many2one('product.product')
    product_tmpl_id = fields.Many2one('product.template')
    sequence = fields.Integer()
    quantity = fields.Float()
    oum_id = fields.Many2one('uom.uom', string='UOM')
    supplierinfo_id = fields.Many2one('product.supplierinfo', "Vendor's product")
    device = fields.Char(company_dependent=True)
