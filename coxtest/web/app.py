import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from coxtest.settings import env_key
from coxtest.web.api import api_router


def create_app(debug=True):
    api_app = FastAPI(title="COXTEST REST API", version="0.1.0", description="COXTEST REST API", debug=debug)

    # CORS 설정
    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    api_app.include_router(api_router, prefix="/api")

    return api_app


if __name__ == "__main__":
    app = create_app()
    host = env_key.WEB_HOST
    port = env_key.WEB_PORT
    uvicorn.run(app, host=host, port=int(port))

