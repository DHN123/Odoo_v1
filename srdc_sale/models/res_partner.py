# -*-coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.addons import base_geolocalize
from odoo.exceptions import UserError
import re


def geo_query_address(street=None, ward=None, district=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(
        field for field in [street, ward, district, state, country] if field
    ))


class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    max_amount = fields.Float(string='Max Amount', digit=(16, 2))
    discount_value = fields.Float(string='Discount (%)', digit=(16, 2))
    is_competitor = fields.Boolean(default=False, string='Is a Competitor')
    district_id = fields.Many2one('res.country.district', string='District')
    ward_id = fields.Many2one('res.country.ward', string='Ward')
    count_contract = fields.Integer(compute='_compute_count_contract')
    count_project = fields.Integer(compute='_compute_count_project')
    full_name = fields.Char('Full name')
    is_company = fields.Boolean(default=True)
    state_id = fields.Many2one("res.country.state", default=lambda self: self.env.ref('l10n_vn.state_vn_VN-SG'))
    country_id = fields.Many2one('res.country', default=lambda self: self.env.ref('base.vn'))
    birthday = fields.Date()
    consultant = fields.Boolean(default=False, string='Consultant')
    investor = fields.Boolean(default=False, string='Investor')
    # department_id = fields.Many2one('hr.department', string='For Department')

    def _compute_count_contract(self):
        for rec in self:
            rec.count_contract = self.env['srdc.contract'].search_count([('partner_id', '=', rec.id)])

    def _compute_count_project(self):
        for rec in self:
            if rec.customer:
                rec.count_project = self.env['project.customer'].search_count([
                    ('partner_id', '=', rec.id)
                ])
            if rec.is_competitor:
                rec.count_project = self.env['project.competitor'].search_count([
                    ('partner_id', '=', rec.id)
                ])
            if rec.consultant:
                rec.count_project = self.env['project.project'].search_count([
                    ('consultant_id', '=', rec.id)
                ])
            if rec.investor:
                rec.count_project = self.env['project.project'].search_count([
                    ('partner_id', '=', rec.id)
                ])

    _sql_constraints = [
        ('name_ref_uniq', 'unique (name, ref)',  "This customer is already exist!"),
    ]

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if not match:
                raise UserError(_("This email is invalid!!!"))
        for rec in self:
            if self.env['res.partner'].search([('email', 'ilike', rec.email)]) \
               or rec.email \
               and rec.email in rec.parent_id.child_ids.filtered(lambda ch: ch.id != rec.id).mapped('email'):
                raise UserError(_("This email is already exist!!!"))

    @api.onchange('mobile')
    def validate_mobile(self):
        for rec in self:
            if rec.mobile and (len(rec.mobile) < 10
               or len(rec.mobile) > 12
               or not rec.mobile[1:].isdecimal()
               or rec.mobile[0] not in ['0', '+']):
                raise UserError(_("This mobile is invalid!!!"))
            if self.env['res.partner'].search([('mobile', 'ilike', rec.mobile)]) \
               or rec.mobile \
               and rec.mobile in rec.parent_id.child_ids.filtered(lambda ch: ch.id != rec.id).mapped('mobile'):
                raise UserError(_("This mobile is already exist!!!"))

    @api.onchange('phone')
    def validate_phone(self):
        for rec in self:
            if rec.phone and (len(rec.phone) < 10
               or len(rec.phone) > 12
               or not rec.phone[1:].isdecimal()
               or rec.phone[0] not in ['0', '+']):
                raise UserError(_("This phone is invalid!!!"))
            if self.env['res.partner'].search([('phone', 'ilike', rec.phone)]) \
               or rec.phone \
               and rec.phone in rec.parent_id.child_ids.filtered(lambda ch: ch.id != rec.id).mapped('phone'):
                raise UserError(_("This phone is already exist!!!"))

    @classmethod
    def _geo_localize(cls, apikey, street='', ward='', district='', state='', country=''):
        search = geo_query_address(street=street, ward=ward, district=district, state=state, country=country)
        # if result is None:
        #     search = geo_query_address(district=district, state=state, country=country)
        #     print(search)
        #     print(apikey)
        #     result = base_geolocalize.models.res_partner(search, apikey)
        return base_geolocalize.models.res_partner.geo_find(search, apikey)

    @api.multi
    def geo_localize(self):
        # We need country names in English below
        apikey = self.env['ir.config_parameter'].sudo().get_param('google.api_key_geocode')
        for partner in self.with_context(lang='en_US'):
            result = partner._geo_localize(
                apikey, partner.street, partner.ward_id.name, partner.district_id.name,
                partner.state_id.name, partner.country_id.name)
            if result:
                partner.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(partner)
                })
        return True
