import re
import logging
import httplib

import view_base
from models import fw_proxy

LOG = logging.getLogger('ryu.gui')

class FwEnable(view_base.ViewBase):
    def __init__(self, host, port, dpid, status=None):
        super(FwEnable, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.status = status

    def run(self):
        LOG.debug('Firewall enable: Enter polling loop')
        return self._dump_status()

    def _dump_status(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': None}

        status = fw_proxy.set_status_enable(address, self.dpid)
        res['status'] = status

        return self.json_response(res)
