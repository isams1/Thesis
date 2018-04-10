import re
import logging
import httplib

import view_base
from models import fw_proxy

LOG = logging.getLogger('ryu.gui')

class FwRuleDelete(view_base.ViewBase):
    def __init__(self, host, port, dpid, rule_id, status=None):
        super(FwRuleDelete, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.rule_id = rule_id
        self.status = status

    def run(self):
        LOG.debug('Firewall Delete Rule running')
        if not self.status:
            # set rule
            return self._delete_rule()

    def _delete_rule(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': None}

        rule_no = {}
        rule_no['rule_id'] = self.rule_id

        status = fw_proxy.delete_firewall_rule(address, rule_no, self.dpid)

        res['status'] = status

        return self.json_response(res)