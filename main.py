from fastapi import FastAPI

from src.api import contact_router, util_router

app = FastAPI()

app.include_router(contact_router, prefix="/api/v1")
app.include_router(util_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
