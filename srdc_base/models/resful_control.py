import ast
import requests

from odoo import tools

headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'charset': 'utf-8',
    'access_token': 'access_token_e8aa0b304d44c824be9dfc84627a7842bf1140f0'
}

qc_data = {
    'db': tools.config['qc_db'],
    'login': tools.config['qc_login'],
    'password': tools.config['qc_pass'],
}


def check_exist(model, host, domain):
    data_return = requests.get(
        '{}/api/{}/'.format(host, model),
        headers=headers,
        data={
            'fields': "['id']",
            'domain': domain
        })
    print(data_return.content)
    return ast.literal_eval(data_return.content.decode('utf-8')).get('data', False)


def sync_user_data(model, vals):
    list_host = [tools.config['qc_host'], ]
    for host in list_host:
        user_id = check_exist(model, host, "[('login', '=', '{}')]".format(vals.get('login', False)))
        if user_id:
            requests.put(
                '{}/api/{}/{}'.format(host, model, user_id[0].get('id', 0)), headers=headers, data=vals)
        else:
            requests.post('{}/api/{}/'.format(host, model), headers=headers, data=vals)


def sync_data_to_qc(model, vals, link_id=None):
    list_host = tools.config['qc_host']
    if link_id:
        requests.put('{}/api/{}/{}'.format(list_host, model, link_id, headers=headers, data=vals))
    else:
        requests.post('{}/api/{}/'.format(list_host, model), headers=headers, data=vals)

