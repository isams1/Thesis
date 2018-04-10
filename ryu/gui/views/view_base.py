import logging
from flask import abort, make_response, jsonify


LOG = logging.getLogger('ryu_gui')


class ViewBase(object):
    def __init__(self, *args, **kwargs):
        pass

    def run(self):
        LOG.error('run() is not defined.')
        abort(500)

    def json_response(self, data):
        return jsonify(**data)

    def null_response(self):
        res = make_response()
        res.headers['Content-type'] = 'text/plain'
        return res
