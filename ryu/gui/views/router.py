import logging
import view_base
from models import rt_proxy

LOG = logging.getLogger('ryu.gui')

class RouterStatusView(view_base.ViewBase):
    def __init__(self, host, port, dpid=None, status=None):
        super(RouterStatusView, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.status = status

    def run(self):
        LOG.debug('Router watching: Enter polling loop')
        if (not self.status and not self.dpid):
            # dump flows
            return self._dump_status()
        elif (not self.status and self.dpid):
            return self._dump_switch_info()

        # TODO: flow-mod
        return self.null_response()

    def _dump_status(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': None}

        status = rt_proxy.get_status(address)
        #for stat in statuses:
        #    status = self._to_client_status(stat.pop('status'))
        #    switch_id = self._to_client_switch_id(stat.pop('switch_id'))
        res['status'] = status

        return self.json_response(res)

    def _dump_switch_info(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': None}

        status = rt_proxy.get_router_addresses(address, self.dpid)
        #for stat in statuses:
        #    status = self._to_client_status(stat.pop('status'))
        #    switch_id = self._to_client_switch_id(stat.pop('switch_id'))
        res['status'] = status

        return self.json_response(res)

    def _to_client_status(self, status):
        return status

    def  _to_client_switch_id(self, dpid):
        return dpid



