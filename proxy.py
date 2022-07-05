import asyncio

import uvicorn
from fastapi import FastAPI
from loguru import logger

from config import Config
from pity_proxy import start_proxy

mock = FastAPI()
if Config.MOCK_ON:
    asyncio.run(start_proxy(logger))

if __name__ == "__main__":
    # uvicorn.run(pity, host="0.0.0.0", port=Config.SERVER_PORT, reload=False)
    uvicorn.run("proxy:mock", host="0.0.0.0", port=Config.PROXY_PORT, reload=False, forwarded_allow_ips="*", workers=1)
