import logging
import json
import httplib

LOG = logging.getLogger('ryu.gui')


_RT_STATUS_PATH_BASE = '/router/all'
_RT_GSDET_ROUTER_PARAMETER = '/router/'



def get_status(address):
    status = []
    try:
        path = '%s' % (_RT_STATUS_PATH_BASE)
        status = json.loads(_do_request(address,'GET', path).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # switch already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return status

def get_router_addresses(address, dpid):
    status = []
    try:
        path = '%s%s' % (_RT_GSDET_ROUTER_PARAMETER, dpid)
        status = json.loads(_do_request(address, 'GET', path).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # switch already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return status

def set_router_parameter(address, body, dpid):
    status = []
    try:
        #path to the proxy server
        path = '%s%s' % (_RT_GSDET_ROUTER_PARAMETER, dpid)
        #status response from the proxy server with read() function will get the body message
        status = json.loads(_do_request(address,'POST', path, body).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # switch already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return status

def delete_router_address(address, address_no, dpid):
    status = []
    try:
        # path to the proxy server
        path = '%s%s' % (_RT_GSDET_ROUTER_PARAMETER, dpid)
        # status response from the proxy server with read() function will get the body message
        status = json.loads(_do_request(address, 'DELETE', path, address_no).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # address already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return status

def delete_router_route(address, route_no, dpid):
    status = []
    try:
        # path to the proxy server
        path = '%s%s' % (_RT_GSDET_ROUTER_PARAMETER, dpid)
        # status response from the proxy server with read() function will get the body message
        status = json.loads(_do_request(address, 'DELETE', path, route_no).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # route already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return status

def _do_request(address, method, action, body=None):
    conn = httplib.HTTPConnection(address)
    headers = {}
    if body is not None:
        body = json.dumps(body)
        headers['Content-Type'] = 'application/json'
    conn.request(method, action, body, headers)
    res = conn.getresponse()
    print(res.status)
    if res.status in (httplib.OK,
                      httplib.CREATED,
                      httplib.ACCEPTED,
                      httplib.NO_CONTENT):
        return res

    raise httplib.HTTPException(
        res, 'code %d reason %s' % (res.status, res.reason),
        res.getheaders(), res.read())
