import logging
import json
import httplib

LOG = logging.getLogger('ryu.gui')


_FW_SGD_FIREWALL_RULES_BASE = '/firewall/rules/'
_FW_STATUS_PATH_BASE = '/firewall/module/status'
_FW_ENABLE_PATH_BASE = '/firewall/module/enable/'
_FW_DISABLE_PATH_BASE = '/firewall/module/disable/'

def delete_firewall_rule(address, body, dpid):
    status = []
    try:
        path = '%s%s' % (_FW_SGD_FIREWALL_RULES_BASE, dpid)
        rule = json.loads(_do_request(address,'DELETE', path, body).read())
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

def get_firewall_rules(address, dpid):
    rule = []
    try:
        path = '%s%s' % (_FW_SGD_FIREWALL_RULES_BASE, dpid)
        rule = json.loads(_do_request(address,'GET', path).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # switch already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return rule


def set_firewall_rules(address, body, dpid):
    status = []
    try:
        #path to the proxy server
        path = '%s%s' % (_FW_SGD_FIREWALL_RULES_BASE, dpid)
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



def get_statuses(address):
    statuses = []
    try:
        path = '%s' % (_FW_STATUS_PATH_BASE)
        statuses = json.loads(_do_request(address,'GET', path).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # switch already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return statuses

def set_status_enable(address, dpid):
    #statuses = []
    try:
        path = '%s%s' % (_FW_ENABLE_PATH_BASE, dpid)
        a = json.loads(_do_request(address,'PUT', path).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # switch already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return a

def set_status_disable(address, dpid):
    #statuses = []
    try:
        path = '%s%s' % (_FW_DISABLE_PATH_BASE, dpid)
        a = json.loads(_do_request(address, 'PUT', path).read())
        #status = json.loads(_do_request(address, 'POST', path).read())
    except IOError as e:
        LOG.error('REST API(%s) is not available.', address)
        raise
    except httplib.HTTPException as e:
        if e[0].status == httplib.NOT_FOUND:
            pass  # switch already deleted
        else:
            LOG.error('REST API(%s, path=%s) request error.', address, path)
            raise
    return a

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
