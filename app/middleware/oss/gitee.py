import base64
import json
from typing import List

import requests
from aioify import aioify

from app.middleware.oss import OssFile


class GiteeOss(OssFile):
    _base_url = "https://gitee.com/api/v5/repos/{}/{}/contents/{}/{}"
    _download_url = "https://gitee.com/api/v5/repos/{}/{}/git/blobs/{}"
    _base_path = "pity"

    def __init__(self, user, repo, token):
        self.user = user
        self.repo = repo
        self.token = token

    @aioify
    async def create_file(self, filepath: str, content: bytes):
        gitee_url = self._base_url.format(self.user, self.repo, self._base_path, filepath)
        data = base64.b64encode(content).decode()
        json_data = {"access_token": self.token, "message": "pity create file", "content": data}
        r = requests.post(url=gitee_url, json=json_data)
        if r.status_code == 400:
            raise Exception("文件重复，请先删除旧文件")
        if r.status_code != 201:
            raise Exception("上传文件到gitee失败")

    @aioify
    async def query_file_by_path(self, filepath: str, ans: List[dict]):
        gitee_url = self._base_url.format(self.user, self.repo, self._base_path, filepath)
        r = requests.get(gitee_url, params=dict(access_token=self.token))
        file_list = r.json()
        for f in file_list:
            if f.get("type") == "file":
                ans.append(dict(key=f.get('path')[5:], download_url=f.get("download_url"),
                                size=0, sha=f.get("sha"),
                                last_modified=None, type='gitee'))
                continue
            await self.query_file_by_path(f"{filepath}/{f.get('name')}", ans)

    # @aioify
    # async def get_size(self, url):
    #     return requests.get(url, stream=True).headers['Content-Length']

    @aioify
    async def update_file(self, filepath: str, content: bytes):
        pass

    @aioify
    async def delete_file(self, filepath: str):
        filepath, sha = filepath.split("$")
        gitee_url = self._base_url.format(self.user, self.repo, self._base_path, filepath)
        r = requests.delete(gitee_url, params=dict(access_token=self.token, message="delete file", sha=sha))
        if r.status_code != 200:
            raise Exception("刪除文件失败")

    @aioify
    async def list_file(self):
        ans = list()
        await self.query_file_by_path("", ans)
        return ans

    @aioify
    async def download_file(self, filepath):
        real_path, sha = filepath.split("$")
        real_filename = real_path.split("/")[-1]
        path = rf'./{self.get_random_filename(real_filename)}'
        data = await self.get_file_object(sha)
        with open(path, 'wb') as f:
            f.write(data)
        return path, real_filename

    @aioify
    async def get_file_object(self, sha):
        """
        :param sha: 文件下载需要的sha值
        :return:
        """
        gitee_url = self._download_url.format(self.user, self.repo, sha)
        r = requests.get(gitee_url)
        data = json.loads(r.content.decode())
        return base64.b64decode(data.get("content").encode())
