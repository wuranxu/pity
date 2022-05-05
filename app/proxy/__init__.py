from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster

from app.proxy.mock import PityMock
from app.proxy.record import PityRecorder
from config import Config


async def start_proxy():
    """
    start mitmproxy server at 7778
    :return:
    """
    addons = [
        PityMock(),
        # PityRecorder()
    ]
    opts = options.Options(listen_host='0.0.0.0', listen_port=Config.MOCK_PORT)
    m = DumpMaster(opts, True, True)
    m.addons.add(*addons)
    await m.run()
