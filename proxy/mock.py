from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster


class AddHeader:
    def __init__(self):
        self.num = 0

    def response(self, flow):
        self.num = self.num + 1
        flow.response.headers["count"] = str(self.num)
        return flow.response


async def start_proxy():
    addons = [
        AddHeader()
    ]
    opts = options.Options(listen_host='0.0.0.0', listen_port=7778)
    m = DumpMaster(opts, False, False)
    m.addons.add(*addons)
    await m.run()
