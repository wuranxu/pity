from fastapi import APIRouter, File, UploadFile, Depends

from app.handler.fatcory import PityResponse
from app.middleware.oss import OssClient
from app.routers import Permission
from config import Config

router = APIRouter(prefix="/oss")


@router.post("/upload")
async def create_oss_file(filepath: str, file: UploadFile = File(...), user_info=Depends(Permission(Config.MEMBER))):
    try:
        file_content = await file.read()
        # 获取oss客户端
        client = OssClient.get_oss_client()
        await client.create_file(filepath, file_content)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(f"上传失败: {e}")


@router.get("/list")
async def list_oss_file(user_info=Depends(Permission(Config.MEMBER))):
    try:
        client = OssClient.get_oss_client()
        files = await client.list_file()
        return PityResponse.success(files)
    except Exception as e:
        return PityResponse.failed(f"获取失败: {e}")


@router.get("/delete")
async def delete_oss_file(filepath: str, user_info=Depends(Permission(Config.MANAGER))):
    try:
        client = OssClient.get_oss_client()
        await client.delete_file(filepath)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(f"删除失败: {e}")


@router.post("/update")
async def update_oss_file(filepath: str, file: UploadFile = File(...), user_info=Depends(Permission(Config.MEMBER))):
    """
    更新oss文件，路径不能变化
    :param user_info:
    :param filepath:
    :param file:
    :return:
    """
    try:
        client = OssClient.get_oss_client()
        file_content = await file.read()
        await client.update_file(filepath, file_content)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(f"删除失败: {e}")


@router.get("/download")
async def download_oss_file(filepath: str):
    """
    更新oss文件，路径不能变化
    :param filepath:
    :return:
    """
    try:
        client = OssClient.get_oss_client()
        # 切割获取文件名
        filename = filepath.split("/")[-1]
        path = await client.download_file(filepath, filename)
        return PityResponse.file(path, filename)
    except Exception as e:
        return PityResponse.failed(f"下载失败: {e}")
