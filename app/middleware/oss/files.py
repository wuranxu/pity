import random
import time
from abc import ABC, abstractmethod
from typing import ByteString


class OssFile(ABC):

    @abstractmethod
    def create_file(self, filepath: str, content: ByteString):
        pass

    @abstractmethod
    def update_file(self, filepath: str, content: ByteString):
        pass

    @abstractmethod
    def delete_file(self, filepath: str):
        pass

    @abstractmethod
    def list_file(self):
        pass

    @abstractmethod
    def download_file(self, filepath, filename):
        pass

    @staticmethod
    def get_random_filename(filename):
        random_str = list("pity")
        random.shuffle(random_str)
        return f"{time.time_ns()}_{''.join(random_str)}_{filename}"
