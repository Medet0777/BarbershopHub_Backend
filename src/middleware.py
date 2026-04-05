import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pyinstrument import Profiler

from src.config import settings

logger = logging.getLogger("bbs")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def profiling(request: Request, call_next):
        if settings.profiling_enabled:
            profiler = Profiler()
            profiler.start()

            response = await call_next(request)

            profiler.stop()

            print(f"\n--- Profile for {request.method} {request.url.path} ---")
            print(profiler.output_text(unicode=True, show_all=False))

            return response

        return await call_next(request)

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        client = request.client
        ip = client.host if client else "unknown"
        port = client.port if client else 0
        method = request.method
        url = request.url.path
        status_code = response.status_code

        message = f"{ip}:{port} - {method} - {url} - {status_code} - {process_time:.4f}s"

        if status_code >= 500:
            logger.error(message)
        elif status_code >= 400:
            logger.error(message)
        elif status_code >= 300:
            logger.debug(message)
        else:
            logger.info(message)

        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:8000",
        ],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"],
    )
