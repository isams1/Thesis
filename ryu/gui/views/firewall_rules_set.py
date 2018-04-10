import re
import logging
import httplib

import view_base
from models import fw_proxy

LOG = logging.getLogger('ryu.gui')

class FwRuleSet(view_base.ViewBase):
    def __init__(self, host, port, dpid, first_host, second_host, proto, action, prior, status=None):
        super(FwRuleSet, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.first_host = first_host
        self.second_host = second_host
        self.proto = proto
        self.action = action
        self.prior = prior
        self.status = status

    def run(self):
        LOG.debug('Firewall Set Rule running')
        if not self.status:
            # set rule
            return self._set_rules()
    def _set_rules(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': []}

        rule_1 = {}
        rule_2 = {}

        #since the ping is bi-directional,  need to add the rule for both ways
        rule_1['nw_src'] = self.first_host
        rule_1['nw_dst'] = self.second_host
        rule_1['actions'] = self.action

        rule_2['nw_src'] = self.second_host
        rule_2['nw_dst'] = self.first_host
        rule_2['actions'] = self.action
        if self.proto:
            rule_1['nw_proto'] = self.proto
            rule_2['nw_proto'] = self.proto
        if (not self.prior or self.prior == "0"):
            pass
        else:
            rule_1['priority'] = self.prior
            rule_2['priority'] = self.prior


        status_1 = fw_proxy.set_firewall_rules(address, rule_1, self.dpid)
        status_2 = fw_proxy.set_firewall_rules(address, rule_2, self.dpid)

        res['status'].append({'status_1': status_1,
                              'status_2': status_2})
        #res.append
        return self.json_response(res)
