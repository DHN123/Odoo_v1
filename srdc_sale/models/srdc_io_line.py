from odoo import api, fields, models


class SRDCIOLine(models.Model):
    _name = "srdc.io.line"

    io_id = fields.Many2one('srdc.io', 'IO')
    product_id = fields.Many2one('product.product', 'Grade')
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
    mix_code = fields.Char()
    amount = fields.Char()
    quantity = fields.Float()
    is_temp = fields.Boolean('Temporary?')
    is_trialmix = fields.Boolean('Is Trial Mix?')
    description = fields.Char()
    # flow_attrs = fields.Many2one(
    #     'product.attribute.value', 'Flow', domain=_get_domain_flow_attrs)
    # slump_attrs = fields.Many2one(
    #     'product.attribute.value', 'Slump', domain=_get_domain_slump_attrs)
    # water_proof_level_attrs = fields.Many2one(
    #     'product.attribute.value', 'Waterproof', domain=_get_domain_water_proof_level_attrs)
    # early_strength_attrs = fields.Many2one(
    #     'product.attribute.value', 'Early Str.', domain=_get_domain_early_strength_attrs)
    # temperature_attrs = fields.Many2one(
    #     'product.attribute.value', 'Temperature', domain=_get_domain_temperature_attrs)
    # def _get_domain_early_strength_attrs(self):
    #     return [('attribute_id', '=', self.env.ref('srdc_sale.product_attribute_category_ear').id)]
    # def _get_domain_temperature_attrs(self):
    #     return [('attribute_id', '=', self.env.ref('srdc_sale.product_attribute_category_tem').id)]
    # def _get_domain_flow_attrs(self):
    #     return [('attribute_id', '=', self.env.ref('srdc_sale.product_attribute_category_flo').id)]
    # def _get_domain_slump_attrs(self):
    #     return [('attribute_id', '=', self.env.ref('srdc_sale.product_attribute_category_slu').id)]
    # def _get_domain_water_proof_level_attrs(self):
    #     return [('attribute_id', '=', self.env.ref('srdc_sale.product_attribute_category_wat').id)]
