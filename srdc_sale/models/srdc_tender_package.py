from odoo import api, fields, models


class SRDCTenderPackage(models.Model):
    _name = "srdc.tender.package"

    name = fields.Char()
