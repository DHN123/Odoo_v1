# -*-coding: utf-8 -*-
from odoo import api, fields, models


class ProjectCustomer(models.Model):
    _name = 'project.customer'

    project_id = fields.Many2one('project.project', string='Project')
    contract_id = fields.Many2one('srdc.contract')
    partner_id = fields.Many2one(
        'res.partner', string='Customer', domain="[('customer','=',1), ('parent_id', '=', False)]")
    partner_manager_id = fields.Many2one('res.partner', string='Project Manager')
    partner_site_id = fields.Many2one('res.partner', string='Site Manager')
    partner_other_id = fields.Many2one('res.partner', string='Other Contact')
    tender_package_id = fields.Many2one('srdc.tender.package', string='Tender Package')
    description = fields.Char()
    user_id = fields.Many2one('res.users', 'Assign to', default=lambda self: self.env.user)

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, '{}'.format(record.project_id.name)))
        return res
