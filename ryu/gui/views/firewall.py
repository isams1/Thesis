import re
import logging
import httplib

import view_base
from models import fw_proxy

LOG = logging.getLogger('ryu.gui')

class FwStatusView(view_base.ViewBase):
    def __init__(self, host, port, statuses=None):
        super(FwStatusView, self).__init__()
        self.host = host
        self.port = port
        self.statuses = statuses

    def run(self):
        LOG.debug('Firewall watching: Enter polling loop')
        if not self.statuses:
            # dump flows
            return self._dump_statuses()

        # TODO: flow-mod
        return self.null_response()

    def _dump_statuses(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'statuses': None}

        statuses = fw_proxy.get_statuses(address)
        #for stat in statuses:
        #    status = self._to_client_status(stat.pop('status'))
        #    switch_id = self._to_client_switch_id(stat.pop('switch_id'))
        res['statuses'] = statuses

        return self.json_response(res)

    def _to_client_status(self, status):
        return status

    def  _to_client_switch_id(self, dpid):
        return dpid



