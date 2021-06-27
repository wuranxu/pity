import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app import pity
from app.routers.auth import user
from app.routers.config import router as config_router
from app.routers.project import project
from app.routers.request import http
from app.routers.testcase import testcase

pity.include_router(user.router)
pity.include_router(project.router)
pity.include_router(http.router)
pity.include_router(testcase.router)
pity.include_router(config_router)

pity.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app='main:pity', host='0.0.0.0', port=7777, reload=False)
