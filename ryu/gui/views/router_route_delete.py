import re
import logging
import httplib

import view_base
from models import rt_proxy

LOG = logging.getLogger('ryu.gui')

class RtRouteDel(view_base.ViewBase):
    def __init__(self, host, port, dpid, route_id, status=None):
        super(RtRouteDel, self).__init__()
        self.host = host
        self.port = port
        self.dpid = dpid
        self.route_id = route_id
        self.status = status

    def run(self):
        LOG.debug('Router Route Delete running')
        if not self.status:
            # set rule
            return self._delete_route()

    def _delete_route(self):
        address = '%s:%s' % (self.host, self.port)
        res = {'host': self.host,
               'port': self.port,
               'status': None}

        route_no = {}
        route_no['route_id'] = self.route_id

        status = rt_proxy.delete_router_route(address, route_no, self.dpid)

        if status[0]['command_result']:
            command_result =  status[0]['command_result']
            res['status'] = command_result
        else:
            res['status'] = status

        res['status'] = status

        return self.json_response(res)