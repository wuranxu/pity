import base64

import requests

from app.middleware.oss import OssFile


class GiteeOss(OssFile):
    _create_url = "https://gitee.com/api/v5/repos/{}/{}/contents/{}"

    def __init__(self, user, repo, token):
        self.user = user
        self.repo = repo
        self.token = token

    def create_file(self, filepath: str, content: bytes):
        gitee_url = self._create_url.format(self.user, self.repo, filepath)
        data = base64.b64encode(content)
        json_data = {"access_token": self.token, "message": "pity create file", "content": data}
        r = requests.post(url=gitee_url, json=json_data)
        if r.status_code != 200:
            raise Exception("上传文件到gitee失败")

    def update_file(self, filepath: str, content: bytes):
        pass

    def delete_file(self, filepath: str):
        pass

    def list_file(self):
        pass

    def download_file(self, filepath, filename):
        pass

    def get_file_object(self, filepath):
        pass
