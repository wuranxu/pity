"""
pity oss文件映射表
"""
from sqlalchemy import String, Column, UniqueConstraint

from app.models.basic import PityBase

units = (
    "B", "KB", "MB", "GB", "TB"
)


class PityOssFile(PityBase):
    # 因为没有目录的概念，都是目录+文件名
    file_path = Column(String(64), nullable=False, index=True, comment="文件路径")
    view_url = Column(String(256), nullable=False, comment="文件预览url")
    file_size = Column(String(16), comment="文件大小")

    __tablename__ = "pity_oss_file"
    __fields__ = (file_path, view_url, file_size)
    __tag__ = "oss"
    __alias__ = dict(file_path="文件路径", view_url="地址", file_size="文件大小")
    __show__ = 1
    __table_args__ = (
        UniqueConstraint('file_path', 'deleted_at'),
    )

    def __init__(self, user, file_path, view_url, file_size, id=None):
        super().__init__(user, id)
        self.file_path = file_path
        self.view_url = view_url
        self.file_size = file_size

    @staticmethod
    def get_size(file_size: int):
        """
        计算文件大小
        :param file_size:
        :return:
        """
        unit_index = 0
        while file_size >= 1024:
            # 说明可以写成kb
            file_size //= 1024
            unit_index += 1
        return f"{file_size}{units[unit_index]}"
