from typing import ByteString

import oss2

from app.middleware.oss.files import OssFile


class AliyunOss(OssFile):

    def __init__(self, access_key_id: str, access_key_secret: str, endpoint: str, bucket: str):
        # auth = oss2.Auth(access_key_id=access_key_id,
        #                  access_key_secret=access_key_secret)
        auth = oss2.AnonymousAuth()
        self.bucket = oss2.Bucket(auth, endpoint, bucket)

    def create_file(self, filepath: str, content: ByteString):
        self.bucket.put_object(filepath, content)

    def update_file(self, filepath: str, content: ByteString):
        self.bucket.put_object(filepath, content)

    def delete_file(self, filepath: str):
        self.bucket.delete_object(filepath)

    def list_file(self):
        ans = []
        for obj in oss2.ObjectIteratorV2(self.bucket):
            ans.append(dict(key=obj.key, last_modified=obj.last_modified,
                            size=obj.size, owner=obj.owner))
        return ans

    def download_file(self, filepath, filename):
        if not self.bucket.object_exists(filepath):
            raise Exception(f"oss文件: {filepath}不存在")
        path = rf'./{self.get_random_filename(filename)}'
        self.bucket.get_object_to_file(filepath, path)
        return path
