from odoo import api, fields, models
from ..models import resful_control


class ChangePasswordUser(models.TransientModel):
    _inherit = 'change.password.user'

    @api.multi
    def change_password_button(self):
        ctx = self._context
        user_id = self.env[ctx.get('active_model')].browse(ctx.get('active_id'))
        for line in self:
            resful_control.sync_data(ctx.get('active_model'), {
                    'login': user_id.login,
                    'password': line.new_passwd,
                })
        super(ChangePasswordUser, self).change_password_button()
