import socket
from functools import lru_cache


# patched version of socket.getfqdn() - see https://github.com/python/cpython/issues/49254
@lru_cache(maxsize=None)
def getfqdn(name=""):
    """Get fully qualified domain name from name.
    An empty argument is interpreted as meaning the local host.
    """
    name = name.strip()
    if not name or name == "0.0.0.0":
        name = socket.gethostname()
    try:
        addrs = socket.getaddrinfo(name, None, 0, socket.SOCK_DGRAM, 0, socket.AI_CANONNAME)
    except OSError:
        pass
    else:
        for addr in addrs:
            if addr[3]:
                name = addr[3]
                break
    return name
