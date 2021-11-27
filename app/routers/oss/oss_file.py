from fastapi import APIRouter, File, UploadFile

from app.handler.fatcory import PityResponse
from app.middleware.oss import OssClient

router = APIRouter(prefix="/oss")


@router.post("/upload")
async def create_oss_file(filepath: str, file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        # 获取oss客户端
        client = OssClient.get_oss_client()
        client.create_file(filepath, file_content)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(f"上传失败: {e}")


@router.get("/list")
async def list_oss_file():
    try:
        client = OssClient.get_oss_client()
        files = client.list_file()
        return PityResponse.success(files)
    except Exception as e:
        return PityResponse.failed(f"获取失败: {e}")


@router.get("/delete")
async def delete_oss_file(filepath: str):
    try:
        client = OssClient.get_oss_client()
        client.delete_file(filepath)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(f"删除失败: {e}")


@router.post("/update")
async def update_oss_file(filepath: str, file: UploadFile = File(...)):
    """
    更新oss文件，路径不能变化
    :param filepath:
    :param file:
    :return:
    """
    try:
        client = OssClient.get_oss_client()
        file_content = await file.read()
        client.update_file(filepath, file_content)
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
        filename = filepath.split("/")[-1]
        path = client.download_file(filepath, filename)
        return PityResponse.file(path, filename)
    except Exception as e:
        return PityResponse.failed(f"删除失败: {e}")
