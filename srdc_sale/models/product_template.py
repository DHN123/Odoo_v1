# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ProductTeamplate(models.Model):
    _inherit = 'product.template'

    def _get_default_category_id(self):
        category = self.env.ref('srdc_sale.concrete_product_category', raise_if_not_found=False)
        if category:
            return category.id
        return super(ProductTeamplate, self)._get_default_category_id()

    astan_code = fields.Char(string='ASTM Code')
    bsen_code = fields.Char(string='BSEN Code')
    bxd_code = fields.Char(string='BXD Code')
    sequence = fields.Integer()
    categ_id = fields.Many2one(
        'product.category', 'Product Category', change_default=True, default=_get_default_category_id, required=True)

    @api.onchange('categ_id')
    def check_create(self):
        for rec in self:
            if rec.categ_id == self.env.ref('srdc_sale.concrete_product_category'):
                attribute_line_data = []
                ear = self.env.ref('srdc_sale.product_attribute_category_ear')
                attribute_line_data.append(
                    (0, 0, {
                        'attribute_id': ear.id,
                        'value_ids': [(6, 0, ear.value_ids.ids)]
                    }))
                flo = self.env.ref('srdc_sale.product_attribute_category_flo')
                attribute_line_data.append(
                    (0, 0, {
                        'attribute_id': flo.id,
                        'value_ids': [(6, 0, flo.value_ids.ids)]
                    }))
                slu = self.env.ref('srdc_sale.product_attribute_category_slu')
                attribute_line_data.append(
                    (0, 0, {
                        'attribute_id': slu.id,
                        'value_ids': [(6, 0, slu.value_ids.ids)]
                    }))
                wat = self.env.ref('srdc_sale.product_attribute_category_wat')
                attribute_line_data.append(
                    (0, 0, {
                        'attribute_id': wat.id,
                        'value_ids': [(6, 0, wat.value_ids.ids)]
                    }))
                ten = self.env.ref('srdc_sale.product_attribute_category_tem')
                attribute_line_data.append(
                    (0, 0, {
                        'attribute_id': ten.id,
                        'value_ids': [(6, 0, ten.value_ids.ids)]
                    }))
                rec.attribute_line_ids = attribute_line_data
