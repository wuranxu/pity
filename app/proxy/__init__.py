from app.proxy.mock import PityMock
from app.proxy.record import PityRecorder
from config import Config


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
        PityMock(),
        # PityRecorder()
    ]
    opts = options.Options(listen_host='0.0.0.0', listen_port=Config.MOCK_PORT)
    m = DumpMaster(opts, True, True)
    m.addons.add(*addons)
    await m.run()
