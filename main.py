from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse

from slowapi.errors import RateLimitExceeded

from src.services import limiter
from src.api import contact_router, health_router, auth_router, user_router

app = FastAPI()
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too many requests. Please try again later"},
    )


app.include_router(auth_router, prefix="/api/v1")
app.include_router(contact_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
