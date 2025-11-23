from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
import secrets

from app.database import get_db
from app.models.user import User
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token

router = APIRouter()

# Initialize OAuth
oauth = OAuth()

# Register Google OAuth
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth is not configured"
        )

    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback"""
    try:
        # Get access token from Google
        token = await oauth.google.authorize_access_token(request)

        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user information from Google"
            )

        email = user_info.get('email')
        google_id = user_info.get('sub')
        full_name = user_info.get('name')

        if not email or not google_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or Google ID not provided"
            )

        # Check if user exists by google_id
        user = db.query(User).filter(User.google_id == google_id).first()

        if not user:
            # Check if user exists by email
            user = db.query(User).filter(User.email == email).first()
            if user:
                # Link existing account with Google
                user.google_id = google_id
                if not user.full_name and full_name:
                    user.full_name = full_name
            else:
                # Create new user
                # Generate username from email
                username = email.split('@')[0]
                # Check if username exists, append random string if needed
                existing_user = db.query(User).filter(User.username == username).first()
                if existing_user:
                    username = f"{username}_{secrets.token_hex(4)}"

                user = User(
                    email=email,
                    username=username,
                    google_id=google_id,
                    full_name=full_name,
                    is_active=True,
                    hashed_password=None  # OAuth users don't have passwords
                )
                db.add(user)

            db.commit()
            db.refresh(user)

        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        # Redirect to frontend with tokens
        # Frontend will extract tokens from URL and store them
        frontend_url = settings.cors_origins[0]
        redirect_url = f"{frontend_url}/auth/callback?access_token={access_token}&refresh_token={refresh_token}"

        return RedirectResponse(url=redirect_url)

    except Exception as e:
        # Redirect to frontend with error
        frontend_url = settings.cors_origins[0]
        error_message = str(e)
        redirect_url = f"{frontend_url}/auth/login?error={error_message}"
        return RedirectResponse(url=redirect_url)
