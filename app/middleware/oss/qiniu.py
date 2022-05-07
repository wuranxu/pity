import os
from io import BytesIO

import aiohttp
from awaits.awaitable import awaitable
from qiniu import Auth, put_stream, BucketManager

from app.middleware.oss import OssFile
from config import Config


class QiniuOss(OssFile):
    _base_path = "pity"

    def __init__(self, access_key_id: str, access_key_secret: str, bucket: str):
        self.auth = Auth(access_key_id, access_key_secret)
        self.bucket = bucket
        self.bucket_manager = BucketManager(self.auth)

    @staticmethod
    def _convert_to_stream(content):
        stream = BytesIO()
        stream.write(content)
        return stream

    @awaitable
    def create_file(self, filepath: str, content: bytes, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        token = self.auth.upload_token(self.bucket, key, 3600)
        file_name = os.path.basename(filepath)
        ret, info = put_stream(token, key, QiniuOss._convert_to_stream(content), file_name, len(content))
        if ret['key'] != key:
            raise Exception("上传失败")
        return QiniuOss.get_url(key), len(content)

    @staticmethod
    def get_url(key):
        return f"{Config.QINIU_URL}/{key}"

    @awaitable
    def update_file(self, filepath: str, content: bytes, base_path: str = None):
        token = self.auth.upload_token(self.bucket, filepath, 3600)
        file_name = os.path.basename(filepath)
        key = self.get_real_path(filepath, base_path)
        ret, info = put_stream(token, key, content, file_name, len(content))
        if ret['key'] != key:
            raise Exception("更新失败")

    @awaitable
    def delete_file(self, filepath: str, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        self.bucket_manager.delete(self.bucket, key)

    async def download_file(self, filepath, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        exists, _ = self.bucket_manager.stat(self.bucket, key)
        if exists is None:
            raise Exception("文件不存在")
        base_url = '%s/%s/%s' % (Config.OSS_URL, self.bucket, filepath)
        url = self.auth.private_download_url(base_url, expires=3600 * 24 * 365)
        content, real_name = await self.download_object(key, url)
        return content, real_name

    async def download_object(self, filepath, url, timeout=15):
        async with aiohttp.ClientSession() as session:
            async with session.request("GET", url, timeout=timeout, ssl=False) as resp:
                if resp.status != 200:
                    raise Exception("download file failed")
                real_filename = filepath.split("/")[-1]
                path = rf'./{self.get_random_filename(real_filename)}'
                with open(path, 'wb') as f:
                    data = await resp.content.read()
                    f.write(data)
                    return path, real_filename

    async def get_file_object(self, filepath):
        key = self.get_real_path(filepath, QiniuOss._base_path)
        exists, _ = self.bucket_manager.stat(self.bucket, key)
        if exists is None:
            raise Exception("文件不存在")
        async with aiohttp.ClientSession() as session:
            basic_url = '%s/%s/%s' % (Config.OSS_URL, self.bucket, filepath)
            async with session.request("GET", basic_url, timeout=15, ssl=False) as resp:
                if resp.status != 200:
                    raise Exception("download file failed")
                return await resp.content.read()
