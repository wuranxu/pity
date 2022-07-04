import asyncio

from app.proxy.mock import PityMock
from app.proxy.record import PityRecorder
from config import Config


def check_port(i):
    import socket, errno
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", i))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("Port is already in use", i)
        else:
            return False
    s.close()
    return True


async def start_proxy(log):
    """
    start mitmproxy server
    :return:
    """
    try:
        from mitmproxy import options
        from mitmproxy.tools.dump import DumpMaster
    except ImportError:
        log.bind(name=None).warning(
            "mitmproxy not installed, Please see: https://docs.mitmproxy.org/stable/overview-installation/")
        return

    addons = [
        PityRecorder()
    ]
    try:
        if Config.MOCK_ON:
            addons.append(PityMock())
        opts = options.Options(listen_host='0.0.0.0', listen_port=Config.PROXY_PORT)
        m = DumpMaster(opts, False, False)
        # remove global block
        block_addon = m.addons.get("block")
        m.addons.remove(block_addon)
        m.addons.add(*addons)
        log.bind(name=None).debug(f"mock server is running at http://0.0.0.0:{Config.PROXY_PORT}")
        await m.run()
    except Exception as e:
        log.bind(name=None).debug(f"mock server running failed, if all nodes run failed, please check: {e}")
