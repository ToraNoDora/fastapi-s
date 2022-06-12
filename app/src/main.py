from fastapi import FastAPI

from src.api.v1.api import api_router
from src.core.config import settings


app = FastAPI(title="FastAPI Demo", description="This is private docs", version="1.0")

app.include_router(api_router, prefix=f"/{settings.API_VERSION_STR}")


if __name__ == "__main__":
        from uvicorn import run
        run("main:app", port=3000, reload=True)

