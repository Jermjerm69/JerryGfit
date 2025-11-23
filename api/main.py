import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings
# Import routers directly to avoid circular import issues on Windows
from app.routers.auth import router as auth_router
from app.routers.risks import router as risks_router
from app.routers.tasks import router as tasks_router
from app.routers.ai import router as ai_router
from app.routers.analytics import router as analytics_router
from app.routers.users import router as users_router
from app.routers.projects import router as projects_router
from app.routers.posts import router as posts_router
from app.routers.oauth import router as oauth_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Custom middleware to handle X-Forwarded-Proto for proper HTTPS redirects
class ForwardedProtoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Trust X-Forwarded-Proto header from reverse proxy
        forwarded_proto = request.headers.get("X-Forwarded-Proto", "")
        if forwarded_proto:
            request.scope["scheme"] = forwarded_proto
        response = await call_next(request)
        return response

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add ForwardedProto middleware first (before CORS)
app.add_middleware(ForwardedProtoMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware (required for OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)

# Create uploads directory if doesn't exist
Path("uploads").mkdir(exist_ok=True)
Path("uploads/profile_pictures").mkdir(parents=True, exist_ok=True)

# Serve static files for profile pictures
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(oauth_router, prefix=f"{settings.API_V1_STR}/oauth", tags=["oauth"])
app.include_router(risks_router, prefix=f"{settings.API_V1_STR}/risks", tags=["risks"])
app.include_router(tasks_router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])
app.include_router(ai_router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])
app.include_router(analytics_router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(projects_router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(posts_router, prefix=f"{settings.API_V1_STR}/posts", tags=["posts"])


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to JerryGFit API",
        "docs": f"{settings.API_V1_STR}/docs",
        "redoc": f"{settings.API_V1_STR}/redoc",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
