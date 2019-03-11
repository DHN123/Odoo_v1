import ast
import json
import werkzeug.wrappers
from odoo import http
from odoo.http import request


_routes = [
    '/api/<model>',
    '/api/<model>/<id>',
    '/api/<model>/<id>/<action>'
]


def valid_response(data, status=200):
    """Valid Response. This will be return when the http request was successfully processed."""
    data = {
        'count': len(data),
        'data': data
    }
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        response=json.dumps(data),
    )


def invalid_response(typ, message=None, status=400):
    """Invalid Response
    This will be the return value whenever the server runs into an error either from the client or the server."""
    return werkzeug.wrappers.Response(
        status=status,
        content_type='application/json; charset=utf-8',
        response=json.dumps({
            'type': typ,
            'message': message if message else 'wrong arguments (missing validation)',
        }),
    )


def extract_arguments(payload, offset=0, limit=0, order=None):
    """."""
    fields, domain = [], []
    if payload.get('domain'):
        domain += ast.literal_eval(payload.get('domain'))
    if payload.get('fields'):
        fields += ast.literal_eval(payload.get('fields'))
    if payload.get('offset'):
        offset = int(payload['offset'])
    if payload.get('limit'):
        limit = int(payload['limit'])
    if payload.get('order'):
        order = payload.get('order')
    return [domain, fields, offset, limit, order]


class APIController(http.Controller):
    """."""
    def __init__(self):
        self._model = 'ir.model'

    @http.route(_routes, type='http', auth="none", methods=['GET'], csrf=False)
    def get(self, model=None, id=None, **payload):
        ioc_name = model
        model = request.env[self._model].sudo().search(
            [('model', '=', model)], limit=1)
        if model:
            domain, fields, offset, limit, order = extract_arguments(payload)
            data = request.env[model.model].sudo().search_read(
                domain=domain, fields=fields, offset=offset, limit=limit, order=order)
            if data:
                return valid_response(data)
            else:
                return valid_response(data)
        return invalid_response('invalid object model', 'The model %s is not available in the registry.' % ioc_name)

    @http.route(_routes, type='http', auth="none", methods=['POST'], csrf=False)
    def create(self, model=None, id=None, **payload):
        """."""
        ioc_name = model
        model = request.env[self._model].sudo().search(
            [('model', '=', model)], limit=1)
        if model:
            try:
                resource = request.env[model.model].sudo().create(payload)
            except Exception as e:
                return invalid_response('params', e)
            else:
                data = {'id': resource.id}
                if resource:
                    return valid_response(data)
                else:
                    return valid_response(data)
        return invalid_response('invalid object model', 'The model %s is not available in the registry.' % ioc_name)

    @http.route(_routes, type='http', auth="none", methods=['PUT'], csrf=False)
    def put(self, model=None, id=None, **payload):
        """."""
        print('==========================================')
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response('invalid object id', 'invalid literal %s for id with base ' % id)
        _model = request.env[self._model].sudo().search(
            [('model', '=', model)], limit=1)
        if not _model:
            return invalid_response('invalid object model', 'The model %s is not available in the registry.' % model,
                                    404)
        try:
            request.env[_model.model].sudo().browse(_id).write(payload)
        except Exception as e:
            return invalid_response('exception', e.name)
        else:
            return valid_response('update %s record with id %s successfully!' % (_model.model, _id))

    @http.route(_routes, type='http', auth="none", methods=['DELETE'], csrf=False)
    def delete(self, model=None, id=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response('invalid object id', 'invalid literal %s for id with base ' % id)
        try:
            record = request.env[model].sudo().search([('id', '=', _id)])
            if record:
                record.unlink()
            else:
                return invalid_response('missing_record', 'record object with id %s could not be found' % _id, 404)
        except Exception as e:
            return invalid_response('exception', e.name, 503)
        else:
            return valid_response('record %s has been successfully deleted' % record.id)

    @http.route(_routes, type='http', auth="none", methods=['PATCH'], csrf=False)
    def patch(self, model=None, id=None, action=None, **payload):
        """."""
        try:
            _id = int(id)
        except Exception as e:
            return invalid_response('invalid object id', 'invalid literal %s for id with base ' % id)
        try:
            record = request.env[model].sudo().search([('id', '=', _id)])
            _callable = action in [method for method in dir(
                record) if callable(getattr(record, method))]
            if record and _callable:
                # action is a dynamic variable.
                getattr(record, action)()
            else:
                return invalid_response(
                    'missing_record',
                    'record object with id %s could not be found or %s object has no method %s' % (
                        _id, model, action), 404)
        except Exception as e:
            return invalid_response('exception', e, 503)
        else:
            return valid_response('record %s has been successfully patched' % record.id)
