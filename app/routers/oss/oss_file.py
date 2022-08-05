from fastapi import APIRouter, File, Depends, UploadFile

from app.crud.auth.UserDao import UserDao
from app.crud.oss.PityOssDao import PityOssDao
from app.handler.fatcory import PityResponse
from app.middleware.oss import OssClient
from app.models.oss_file import PityOssFile
from app.routers import Permission, get_session
from config import Config

router = APIRouter(prefix="/oss")


@router.post("/upload")
async def create_oss_file(filepath: str, file: UploadFile = File(...),
                          session=Depends(get_session),
                          user_info=Depends(Permission(Config.MEMBER))):
    try:
        file_content = await file.read()
        client = OssClient.get_oss_client()
        # oss上传 WARNING: 可能存在数据不同步的问题，oss成功本地失败
        file_url, file_size = await client.create_file(filepath, file_content)
        # 本地数据也要备份一份
        model = PityOssFile(user_info['id'], filepath, file_url, PityOssFile.get_size(file_size))
        record = await PityOssDao.query_record(file_path=filepath,
                                               deleted_at=0)
        if record is not None:
            record.file_path = filepath
            record.view_url = file_url
            record.file_size = file_size
            await PityOssDao.update_record_by_id(user_info['id'], record)
        else:
            await PityOssDao.insert(model=model, log=True)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(f"上传失败: {e}")


@router.post("/avatar", summary="上传用户头像")
async def upload_avatar(file: UploadFile = File(...), user_info=Depends(Permission(Config.MEMBER))):
    try:
        file_content = await file.read()
        suffix = file.filename.split(".")[-1]
        filepath = f"user_{user_info['id']}.{suffix}"
        client = OssClient.get_oss_client()
        file_url, _ = await client.create_file(filepath, file_content, base_path="avatar")
        await UserDao.update_avatar(user_info['id'], file_url)
        return PityResponse.success(file_url)
    except Exception as e:
        return PityResponse.failed(f"上传头像失败: {e}")


@router.get("/list")
async def list_oss_file(filepath: str = '', _=Depends(Permission(Config.MEMBER))):
    try:
        records = await PityOssDao.select_list(condition=[PityOssFile.file_path.like(f'%{filepath}%')])
        return PityResponse.records(records)
    except Exception as e:
        return PityResponse.failed(f"获取失败: {e}")


@router.get("/delete")
async def delete_oss_file(filepath: str, user_info=Depends(Permission(Config.MANAGER)), session=Depends(get_session)):
    try:
        # 先获取到本地的记录，拿到sha值
        record = await PityOssDao.query_record(file_path=filepath, deleted_at=0)
        if record is None:
            raise Exception("文件不存在或已被删除")
        await PityOssDao.delete_record_by_id(session, user_info["id"], record.id, log=True)
        client = OssClient.get_oss_client()
        await client.delete_file(filepath)
        return PityResponse.success()
    except Exception as e:
        return PityResponse.failed(f"删除失败: {e}")


# @router.post("/update")
# async def update_oss_file(filepath: str, file: UploadFile = File(...), user_info=Depends(Permission(Config.MEMBER))):
#     """
#     更新oss文件，路径不能变化
#     :param user_info:
#     :param filepath:
#     :param file:
#     :return:
#     """
#     try:
#         client = OssClient.get_oss_client()
#         file_content = await file.read()
#         await client.update_file(filepath, file_content)
#         return PityResponse.success()
#     except Exception as e:
#         return PityResponse.failed(f"修改失败: {e}")


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
        path, filename = await client.download_file(filepath)
        return PityResponse.file(path, filename)
    except Exception as e:
        return PityResponse.failed(f"下载失败: {e}")
