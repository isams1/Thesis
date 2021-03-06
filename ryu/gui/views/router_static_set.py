import logging
import view_base
from models import rt_proxy

LOG = logging.getLogger('ryu.gui')

class RtStaticSetView(view_base.ViewBase):
    def __init__(self, host, port, dpid, destination, gateway, status=None):
        super(RtStaticSetView, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.destination = destination
        self.gateway = gateway
        self.status = status

    def run(self):
        LOG.debug('Router Static Route Setting: Enter polling loop')
        if not self.status:
            # dump flows
            return self._dump_status()

        # TODO: flow-mod
        return self.null_response()

    def _dump_status(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': None}

        rt_static = {}
        rt_static['destination'] = self.destination
        rt_static['gateway'] = self.gateway

        status = rt_proxy.set_router_parameter(address, rt_static, self.dpid)
        #for stat in statuses:
        #    status = self._to_client_status(stat.pop('status'))
        #    switch_id = self._to_client_switch_id(stat.pop('switch_id'))
        if status[0]['command_result']:
            command_result =  status[0]['command_result']
            res['status'] = command_result
        else:
            res['status'] = status

        return self.json_response(res)

    def _to_client_status(self, status):
        return status

    def  _to_client_switch_id(self, dpid):
        return dpid



