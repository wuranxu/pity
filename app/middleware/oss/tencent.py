from awaits.awaitable import awaitable
from qcloud_cos import CosConfig, CosS3Client

from app.middleware.oss import OssFile


class TencentCos(OssFile):
    _base_path = "pity"

    def __init__(self, access_key_id: str, access_key_secret: str, region: str, bucket: str):
        self.bucket = bucket
        self.config = CosConfig(Region=region, SecretId=access_key_id, SecretKey=access_key_secret)
        self.client = CosS3Client(self.config)

    @awaitable
    def create_file(self, filepath: str, content: bytes, base_path: str = None):
        try:
            key = self.get_real_path(filepath, base_path)
            self.client.put_object(
                Bucket=self.bucket,
                Body=content,
                Key=key,
            )
            res = self.client.get_object_url(self.bucket, key)
            return res, len(content)
        except Exception as e:
            raise Exception(f"上传出错: {e}")

    @awaitable
    def update_file(self, filepath: str, content: bytes, base_path: str = None):
        return self.create_file(filepath, content, base_path)

    @awaitable
    def delete_file(self, filepath: str, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        self.client.delete_object(self.bucket, key)

    def list_file(self):
        pass

    @awaitable
    def download_file(self, filepath, base_path: str = None):
        key = self.get_real_path(filepath, base_path)
        real_filename = filepath.split("/")[-1]
        path = rf'./{self.get_random_filename(real_filename)}'
        self.client.download_file(
            Bucket=self.bucket,
            Key=key,
            DestFilePath=path
        )
        return path, real_filename

    @awaitable
    def get_file_object(self, filepath):
        key = self.get_real_path(filepath)
        response = self.client.get_object(
            Bucket=self.bucket,
            Key=key
        )
        return response['Body'].read()
