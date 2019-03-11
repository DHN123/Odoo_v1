# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ConcretePumpAttrCategory(models.Model):
    _name = 'srdc.concrete.pump.category'

    name = fields.Many2one('srdc.type.of.pump', string='Loại Bơm', required=True)
    floor_elevation = fields.Many2one('srdc.floor.elevation', string='Cao Độ Sàn', required=True)
    order_pump = fields.Many2one('srdc.concrete.pump.volume', string="Khối Lượng Bơm(m3)", required=True)
    block_m3_nail = fields.Float(string="Khối Lượng Bơm VAT 10%, >Khối Lượng Bơm(vnd/m3)/Bơm móng, sàn", required=True)
    block_m3_component = fields.Float(string="Khối Lượng Bơm VAT 10%, >Khối Lượng Bơm(vnd/m3)/Bơm cấu kiện", required=True)
    block_times_nail = fields.Float(string="Khối Lượng Bơm VAT 10%, <=Khối Lượng Bơm(vnd/lần)/Bơm móng, sàn")
    block_times_component = fields.Float(string="Khối Lượng Bơm VAT 10%, <=Khối Lượng Bơm(vnd/lần)/Bơm cấu kiện")
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    selection = fields.Boolean()

    @api.onchange('order_pump', 'block_m3_nail', 'block_m3_component')
    def compute_check_block_m3_nail(self):
        for rec in self:
            if rec.order_pump:
                rec.block_times_nail = rec.block_m3_nail * rec.order_pump.name
                rec.block_times_component = rec.block_m3_component * rec.order_pump.name

    # complete_name = fields.Char(
    #     'Attributes', compute='_compute_complete_name',
    #     store=True)
    # parent_id = fields.Many2one('concrete.pump.category', index=True, string='Parent Cateogry')
    # parent_path = fields.Char(index=True)
    # values = fields.Char()
    # visible = fields.Boolean()
    # sequence = fields.Integer()
    #
    # @api.depends('name', 'parent_id.complete_name')
    # def _compute_complete_name(self):
    #     for category in self:
    #         if category.parent_id:
    #             category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
    #         else:
    #             category.complete_name = category.name
