from pymock import Mock


class PityMock(object):
    def __init__(self):
        self.mock = Mock()

    def request(self, flow):
        pass
        # if flow.request.pretty_url.startswith("http://www.baidu.com"):
        #     data = self.mock.mock_js("""
        #     {
        #         name: {
        #             first: "@cfirst",
        #             last: "@clast",
        #             name: "@first@last",
        #         }
        #     }
        #     """)
        #     flow.response = http.Response.make(
        #         200,  # (optional) status code
        #         json.dumps(data, ensure_ascii=False, indent=4),  # (optional) content
        #         {"Content-Type": "application/json"}  # (optional) headers
        #     )
