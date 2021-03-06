###################################################################################
#
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ----------------------------------------------------------
    # Selections
    # ----------------------------------------------------------

    def _attachment_location_selection(self):
        locations = self.env['ir.attachment'].storage_locations()
        return list(map(lambda location: (location, location.upper()), locations))

    # ----------------------------------------------------------
    # Database
    # ----------------------------------------------------------

    attachment_location = fields.Selection(
        selection=_attachment_location_selection,
        string='Storage Location',
        required=True,
        help="Attachment storage location.")

    # ----------------------------------------------------------
    # Functions
    # ----------------------------------------------------------

    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('ir_attachment.location', self.attachment_location)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(attachment_location=params.get_param('ir_attachment.location', 'file'))
        return res

    @api.multi
    def attachment_force_storage(self):
        self.env['ir.attachment'].force_storage()
