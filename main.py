from fastapi import FastAPI
from routers import template_public_router
import os

IS_PROD=os.getenv("IS_PROD", "false").lower() == "true"

app=FastAPI(
    docs_url="/docs" if not IS_PROD else None,
    redoc_url="/redoc" if not IS_PROD else None,
    openapi_url="/openapi.json" if not IS_PROD else None
)

@app.get("/")
def read_root():
    return {"Hello":"World"}

app.include_router(template_public_router.router)