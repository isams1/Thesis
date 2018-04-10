#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import logging
import inspect
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, abort, g, jsonify
from views.view_base import ViewBase

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth


parser = ArgumentParser()
parser.add_argument('--host', dest='host', default='0.0.0.0')
parser.add_argument('--port', dest='port', type=int, default=8000)
args = parser.parse_args()

app = Flask(__name__.split('.')[0])
logging.basicConfig(level=logging.DEBUG,
                    stream=sys.stderr,
                    format="%(asctime)-15s [%(levelname)-4s] %(message)s")
#handler = logging.FileHandler("/tmp/ryu_gui.log", encoding="utf8")
#app.logger.addHandler(handler)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

background_tasks = {}
app.config['AUTO_DELETE_BG_TASKS'] = True

class ValidationError(ValueError):
    pass

# The two password function came with Flask Werkzeug
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# g is the context request object from Flask
@auth.verify_password
def verify_password(username, password):
    g.user = User.query.filter_by(username=username).first()
    if g.user is None:
        return False
    return g.user.verify_password(password)

@app.before_request
@auth.login_required
def before_request_trigger():
    pass

@auth.error_handler
def unathorized():
    response = jsonify({'status': 401, 'error': 'unahtorized',
                        'message': 'please authenticate'})
    response.status_code = 401
    return response

@app.after_request
def after_request_trigger(response):
    return response


@app.route('/')
def index():
    return _view('topology')


@app.route('/stats/flow', methods=['POST'])
def flow_mod():
    return _view('flow', request.form.get('host'), request.form.get('port'),
                 request.form.get('dpid'), request.form.get('flows'))

@app.route('/firewall/module/status', methods=['POST'])
def firewall_status_mod():
    return _view('firewall', request.form.get('host'), request.form.get('port'))

@app.route('/firewall/module/enable', methods=['POST'])
def firewall_enable():
    return _view('firewall_enable', request.form.get('host'), request.form.get('port'),
                 request.form.get('dpid'),request.form.get('status'))

@app.route('/firewall/module/disable', methods=['POST'])
def firewall_disable():
    return _view('firewall_disable', request.form.get('host'), request.form.get('port'),
                 request.form.get('dpid'), request.form.get('status'))

@app.route('/firewall/rules', methods=['POST'])
def firewall_rules_get():
    return _view('firewall_rules_get', request.form.get('host'), request.form.get('port'), request.form.get('dpid'))

@app.route('/firewall/rules/set', methods=['POST'])
def firewall_rules_set():
    return _view('firewall_rules_set', request.form.get('host'), request.form.get('port'), request.form.get('dpid'), request.form.get('1st_host'), request.form.get('2nd_host'),
                 request.form.get('proto'), request.form.get('action'), request.form.get('prior'))

@app.route('/firewall/rule/delete', methods=['POST'])
def firewall_rule_delete():
    return _view('firewall_rule_delete', request.form.get('host'), request.form.get('port'), request.form.get('dpid'), request.form.get('rule_id'))

@app.route('/router/status', methods=['POST'])
def router_status_mod():
    return _view('router', request.form.get('host'), request.form.get('port'))

@app.route('/router/addresses', methods=['POST'])
def router_addresses_per_switch_get():
    return _view('router', request.form.get('host'), request.form.get('port'), request.form.get('dpid'))

@app.route('/router/routes', methods=['POST'])
def router_routes_per_switch_get():
    return _view('router', request.form.get('host'), request.form.get('port'), request.form.get('dpid'))

@app.route('/router/address', methods=['POST'])
def router_address_set():
    return _view('router_address_set', request.form.get('host'), request.form.get('port'), request.form.get('dpid'), request.form.get('address'))

@app.route('/router/static', methods=['POST'])
def router_static_set():
    return _view('router_static_set', request.form.get('host'), request.form.get('port'), request.form.get('dpid'), request.form.get('destination'), request.form.get('gateway'))

@app.route('/router/default', methods=['POST'])
def router_default_set():
    return _view('router_default_set', request.form.get('host'), request.form.get('port'), request.form.get('dpid'), request.form.get('gateway'))

@app.route('/router/address/delete', methods=['POST'])
def router_address_del():
    return _view('router_address_delete', request.form.get('host'), request.form.get('port'), request.form.get('dpid'), request.form.get('address_id'))

@app.route('/router/route/delete', methods=['POST'])
def router_route_del():
    return _view('router_route_delete', request.form.get('host'), request.form.get('port'), request.form.get('dpid'), request.form.get('route_id'))


@app.route('/websocket')
def websocket():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        return _view('websocket', ws)
    abort(404)


def _view(view_name, *args, **kwargs):
    view_name = 'views.' + view_name
    try:
        __import__(view_name)
    except ImportError:
        app.logger.error('ImportError (%s)', view_name)
        abort(500)

    mod = sys.modules.get(view_name)
    clases = inspect.getmembers(mod, lambda cls: (inspect.isclass(cls) and
                                                  issubclass(cls, ViewBase)))
    try:
        view = clases[0][1](*args, **kwargs)
    except IndexError:
        app.logger.error('has not View class (%s)', view_name)
        abort(500)
    app.logger.debug('view loaded. %s', view_name)
    return view.run()


if __name__ == '__main__':
    server = pywsgi.WSGIServer((args.host, args.port),
                               app, handler_class=WebSocketHandler)
    app.logger.info('Running on %s', server.address)
    server.serve_forever()
