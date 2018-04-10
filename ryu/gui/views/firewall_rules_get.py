import re
import logging
import httplib

import view_base
from models import fw_proxy

LOG = logging.getLogger('ryu.gui')

class FwRuleGet(view_base.ViewBase):
    def __init__(self, host, port, dpid, status=None):
        super(FwRuleGet, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.status = status

    def run(self):
        LOG.debug('Firewall Get Rule running')
        if not self.status:
            # set rule
            return self._get_rules()

    def _get_rules(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'rules': None}

        rules = fw_proxy.get_firewall_rules(address, self.dpid)

        res['rules'] = rules

        return self.json_response(res)