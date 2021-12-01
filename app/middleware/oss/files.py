import random
import time
from abc import ABC, abstractmethod
from typing import ByteString


class OssFile(ABC):

    @abstractmethod
    async def create_file(self, filepath: str, content: bytes):
        pass

    @abstractmethod
    async def update_file(self, filepath: str, content: bytes):
        pass

    @abstractmethod
    async def delete_file(self, filepath: str):
        pass

    @abstractmethod
    async def list_file(self):
        pass

    @abstractmethod
    async def download_file(self, filepath, filename):
        pass

    @abstractmethod
    async def get_file_object(self, filepath):
        pass

    @staticmethod
    def get_random_filename(filename):
        random_str = list("pity")
        random.shuffle(random_str)
        return f"{time.time_ns()}_{''.join(random_str)}_{filename}"
