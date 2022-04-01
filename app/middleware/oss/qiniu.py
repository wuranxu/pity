import os
from io import BytesIO

from qiniu import Auth, put_stream, BucketManager
from qiniu.services.cdn.manager import create_timestamp_anti_leech_url
from app.middleware.oss import OssFile
from config import Config


class QiniuOss(OssFile):
    _base_path = "pity"

    def __init__(self, access_key_id: str, access_key_secret: str, bucket: str):
        self.auth = Auth(access_key_id, access_key_secret)
        self.bucket = bucket
        self.bucket_manager = BucketManager(self.auth)

    def get_full_path(self, filepath, base_path: str = None):
        base_path = base_path if base_path is not None else self._base_path
        return f"{base_path}/{filepath}"

    @staticmethod
    def _convert_to_stream(content):
        stream = BytesIO()
        stream.write(content)
        return stream

    async def create_file(self, filepath: str, content: bytes, base_path: str = None):
        key = self.get_full_path(filepath, base_path)
        token = self.auth.upload_token(self.bucket, key, 3600)
        file_name = os.path.basename(filepath)
        ret, info = put_stream(token, key, QiniuOss._convert_to_stream(content), file_name, len(content))
        if ret['key'] != key:
            raise Exception("上传失败")
        return self.get_url(key), len(content), None

    def get_url(self, key):
        return f"http://oss.pity.fun/{key}"

    async def update_file(self, filepath: str, content: bytes, base_path: str = None):
        token = self.auth.upload_token(self.bucket, filepath, 3600)
        file_name = os.path.basename(filepath)
        key = self.get_full_path(filepath, base_path)
        ret, info = put_stream(token, key, content, file_name, len(content))
        if ret['key'] != key:
            raise Exception("更新失败")

    async def delete_file(self, filepath: str):
        self.bucket_manager.delete(self.bucket, filepath)

    async def list_file(self):
        ret, eof, info = self.bucket_manager.list(self.bucket, self._base_path)
        return ret.get('items')

    async def download_file(self, filepath):
        base_url = '%s/%s/%s' % (Config.OSS_URL, self.bucket, filepath)
        url = self.auth.private_download_url(base_url, expires=3600)
        # data = self.bucket_manager.fetch(base_url, filepath)
        print(url)
        return url, None

    async def get_file_object(self, filepath):
        pass
        # if not self.bucket.object_exists(filepath):
        #     raise Exception(f"oss文件: {filepath}不存在")
        # file_object = self.bucket.get_object(filepath)
        # return file_object.resp.response.content
