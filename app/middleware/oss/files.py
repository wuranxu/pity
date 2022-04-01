import random
import time
from abc import ABC, abstractmethod


class OssFile(ABC):
    _base_path = "pity"

    @abstractmethod
    async def create_file(self, filepath: str, content, base_path: str = None) -> (str, int, str):
        pass

    @abstractmethod
    async def update_file(self, filepath: str, content, base_path: str = None):
        pass

    @abstractmethod
    async def delete_file(self, filepath: str):
        pass

    @abstractmethod
    async def list_file(self):
        pass

    @abstractmethod
    async def download_file(self, filepath):
        pass

    @abstractmethod
    async def get_file_object(self, filepath):
        pass

    async def get_real_path(self, filepath, base_path=None):
        return f"{self._base_path if base_path is None else base_path}/{filepath}"

    @staticmethod
    def get_random_filename(filename):
        random_str = list("pity")
        random.shuffle(random_str)
        return f"{time.time_ns()}_{''.join(random_str)}_{filename}"
