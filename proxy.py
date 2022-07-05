import asyncio

from fastapi import FastAPI

from app.proxy import start_proxy
from config import Config
from main import logger

mock = FastAPI()
if Config.MOCK_ON:
    asyncio.run(start_proxy(logger))
