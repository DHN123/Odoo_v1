from odoo import api, fields, models, tools
from . import resful_control


class Users(models.Model):
    _inherit = "res.users"

    # @api.model
    # def create(self, vals):
    #     res = super(Users, self).create(vals)
    #     self.sync_user_data(vals)
    #     return res

    # @api.multi
    # def write(self, vals):
    #     res = super(Users, self).write(vals)
    #     self.sync_user_data(vals)
    #     import traceback
    #     traceback.print_stack()
    #     return res

    @api.multi
    def action_sync_data(self):
        self.env.cr.execute("""
                    SELECT u.login, u.active, p.email, p.phone, p.mobile, p.type, p.name
                    FROM res_users u, res_partner p
                    WHERE u.id in {}
                    AND u.partner_id = p.id
                """.format(tuple(self.mapped('id') + [0, 0])))
        for user in self.env.cr.fetchall():
            vals = {
                'login': user[0],
                'active': user[1],
                'email': user[2],
                'phone': user[3],
                'mobile': user[4],
                'type': user[5],
                'name': user[6],
            }
            resful_control.sync_user_data(self._name, vals)

    @api.model
    def change_password(self, old_passwd, new_passwd):
        resful_control.sync_user_data(self._name, {
            'login': self.env.user.login,
            'password': new_passwd,
        })
        return super(Users, self).change_password(old_passwd=old_passwd, new_passwd=new_passwd)

    @api.model
    def signup(self, values, token=None):
        resful_control.sync_user_data(self._name, values)
        return super(Users, self).signup(values, token)
