from odoo import api, fields, models, exceptions


class SRDCMixDesign(models.Model):
    _name = "srdc.mix.design"

    name = fields.Char()
    active = fields.Boolean(default=True)
    product_id = fields.Many2one('product.product')
    product_qty = fields.Float(default=1)
    sequence = fields.Integer()
    line_ids = fields.One2many('srdc.mix.design.line', 'mix_design_id', srting='Mix_Design')
    is_auto = fields.Boolean()
    total_amount = fields.Float(compute='_compute_total_amount', store=True)
    optimize_total_amount = fields.Float(compute='_compute_total_amount', store=True)
    is_standard = fields.Boolean('Standard?')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('lab_test', 'LAB Test'),
        ('validated', 'Validated'),
        ('done', 'Done'),
        ('pending', 'Pending'),
        ('cancel', 'Cancel'),
    ], default='draft')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Code name already exists !"),
    ]

    @api.model
    def create(self, vals):
        if not self.search([('is_standard', '=', True)]) and not vals.get('is_standard'):
            vals['is_standard'] = True
        return super(SRDCMixDesign, self).create(vals)

    @api.model
    def default_get(self, fields):
        defaults = super(SRDCMixDesign, self).default_get(fields)
        material_ids = self.env['product.product'].search([
            ('categ_id.parent_id', '=', self.env.ref('srdc_qc.product_category_material').id)
        ], order='id')
        defaults['line_ids'] = [
            (0, 0, {
                'product_id': material.id,
                'product_tmpl_id': material.product_tmpl_id.id,
                'categ_id': material.categ_id.id,
                'quantity': 0,
                'sequence': material.id,
                'oum_id': material.uom_id.id
            }) for material in material_ids]
        return defaults

    @api.multi
    @api.depends('line_ids.quantity', 'line_ids.product_id', 'line_ids.product_id.standard_price',
                 'line_ids.supplierinfo_id', 'line_ids.supplierinfo_id.price')
    def _compute_total_amount(self):
        for rec in self:
            sum = 0
            optimize_sum = 0
            for line in rec.line_ids.filtered(
                    lambda l: l.quantity > 0 and (
                            l.product_id.standard_price > 0 or l.supplierinfo_id and l.supplierinfo_id.price > 0)):
                if line.supplierinfo_id:
                    sum += line.supplierinfo_id.price * line.quantity
                    optimize_sum += line.supplierinfo_id.optimize_price * line.quantity
                else:
                    sum += line.product_id.standard_price * line.quantity
                    optimize_sum += line.product_id.optimize_price * line.quantity
            rec.total_amount = sum
            rec.optimize_total_amount = optimize_sum

    @api.multi
    def btn_confirm(self):
        self.write({'state': 'confirmed'})

    @api.multi
    def btn_start_lab_test(self):
        self.write({'state': 'lab_test'})

    @api.multi
    def btn_validate(self):
        self.write({'state': 'validated'})

    @api.multi
    def btn_approve(self):
        self.write({'state': 'done'})

    @api.multi
    def btn_set_to_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def btn_cancel(self):
        self.write({'state': 'cancel'})
