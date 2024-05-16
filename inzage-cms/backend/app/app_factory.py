import logging

import secure
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


def create_app():
    secure_headers = secure.Secure()

    logger.info("Creating app.")
    app = FastAPI(
        title="inzage-cms",
        description="inzage_beheer_module",
        docs_url="/api-docs",
        redoc_url=None,
    )

    logger.info("Adding middlewares.")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info("Adding API router.")
    from app.api.api import router as api_router

    app.include_router(api_router, prefix="/api")

    @app.middleware("http")
    async def set_secure_headers(request, call_next):
        """
        Middleware that adds security headers to each request.
        """
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        return response

    return app
