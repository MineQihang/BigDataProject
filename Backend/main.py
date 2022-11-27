from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 跨域

from SingleVideoInfo import single_video

app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(single_video.router)

origins = ["*"] # 跨域

app.add_middleware( # 跨域
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 默认api
@app.get('/')
async def index():
    return {"code": 200, "msg": "Hello, this is the api of our project!"}
