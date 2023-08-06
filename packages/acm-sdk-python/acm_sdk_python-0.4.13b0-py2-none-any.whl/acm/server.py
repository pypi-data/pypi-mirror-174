import socket
import logging
import random

try:
    # python3.6
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    # python2.7
    from urllib2 import Request, urlopen, URLError

logger = logging.getLogger("acm")

ADDRESS_URL_PTN = "http://%s/diamond-server/diamond"
ADDRESS_URL_PTN_FOR_UNIT = "http://%s/diamond-server/diamond-unit-%s?nofix=1"

ADDRESS_SERVER_TIMEOUT = 3  # in seconds


def is_ipv4_address(address):
    try:
        socket.inet_aton(address)
    except socket.error:
        return False
    return True


def parse_nacos_server_addr(server_addr):
    sp = server_addr.split(":")
    if len(sp) == 3:
        return sp[0] + ":" + sp[1], int(sp[2])
    else:
        port = int(sp[1]) if len(sp) > 1 else 8080
        return sp[0], port, True


def get_server_list(endpoint, default_port=8080, cai_enabled=True, unit_name=None):
    server_list = list()

    import os
    server_addresses = os.getenv('DIAMOND_SERVER_IPS')
    for server_addr in server_addresses.split(","):
        if server_addr is not "" and parse_nacos_server_addr(server_addr):
            server_list.append(parse_nacos_server_addr(server_addr.strip()))
    if len(server_list) > 0:
        return server_list


    if not cai_enabled:
        logger.info("[get-server-list] cai server is not used, regard endpoint:%s as server." % endpoint)
        content = endpoint.encode()
    else:
        try:
            # use 8080 as default port.
            if ":" not in endpoint:
                endpoint = endpoint + ":8080"

            url = ADDRESS_URL_PTN % endpoint

            if unit_name:
                logger.info("[get-server-list] getting server for unit:%s" % unit_name)
                url = ADDRESS_URL_PTN_FOR_UNIT % (endpoint, unit_name)

            content = urlopen(url, timeout=ADDRESS_SERVER_TIMEOUT).read()
            logger.debug("[get-server-list] content from endpoint:%s" % content)
        except (URLError, OSError, socket.timeout) as e:
            logger.error("[get-server-list] get server from %s failed, cause:%s" % (endpoint, e))
            return server_list

    if content:
        for server_info in content.decode().strip().split("\n"):
            sp = server_info.strip().split(":")
            if len(sp) == 1:
                server_list.append((sp[0], default_port, is_ipv4_address(sp[0])))
            else:
                try:
                    server_list.append((sp[0], int(sp[1]), is_ipv4_address(sp[0])))
                except ValueError:
                    logger.warning("[get-server-list] bad server address:%s ignored" % server_info)

    random.shuffle(server_list)

    return server_list
