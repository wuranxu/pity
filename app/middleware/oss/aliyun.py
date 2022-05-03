import oss2
from awaits.awaitable import awaitable

from app.middleware.oss.files import OssFile


class AliyunOss(OssFile):

    def __init__(self, access_key_id: str, access_key_secret: str, endpoint: str, bucket: str):
        auth = oss2.Auth(access_key_id=access_key_id,
                         access_key_secret=access_key_secret)
        # auth = oss2.AnonymousAuth()
        self.bucket = oss2.Bucket(auth, endpoint, bucket)

    @awaitable
    def create_file(self, filepath: str, content: bytes, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        response = self.bucket.put_object(key, content)
        return response.resp.response.url, len(content)

    @awaitable
    def delete_file(self, filepath: str, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        self.bucket.delete_object(key)

    @awaitable
    def download_file(self, filepath, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        filename = key.split("/")[-1]
        if not self.bucket.object_exists(filepath):
            raise Exception(f"oss文件: {filepath}不存在")
        path = rf'./{self.get_random_filename(filename)}'
        self.bucket.get_object_to_file(filepath, path)
        return path, filename

    @awaitable
    def get_file_object(self, filepath):
        key = self.get_real_path(filepath)
        if not self.bucket.object_exists(key):
            raise Exception(f"oss文件: {key}不存在")
        file_object = self.bucket.get_object(key)
        return file_object.resp.response.content
