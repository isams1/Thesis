import re
import logging
import httplib

import view_base
from models import rt_proxy

LOG = logging.getLogger('ryu.gui')

class RtAddrDel(view_base.ViewBase):
    def __init__(self, host, port, dpid, address_id, status=None):
        super(RtAddrDel, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.address_id = address_id
        self.status = status

    def run(self):
        LOG.debug('Router Address Delete Rule running')
        if not self.status:
            # set rule
            return self._delete_address()

    def _delete_address(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': None}

        address_no = {}
        address_no['address_id'] = self.address_id

        status = rt_proxy.delete_router_address(address, address_no, self.dpid)

        if status[0]['command_result']:
            command_result =  status[0]['command_result']
            res['status'] = command_result
        else:
            res['status'] = status

        res['status'] = status

        return self.json_response(res)