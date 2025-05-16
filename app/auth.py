# app/auth.py
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")  # e.g. https://yourdomain.com/api/auth/callback
OAUTH_URL = "https://discord.com/api/oauth2/authorize"
TOKEN_URL = "https://discord.com/api/oauth2/token"
USER_URL = "https://discord.com/api/users/@me"

SCOPES = "identify email guilds"

@router.get("/login")
def login():
    url = (
        f"{OAUTH_URL}?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPES}"
    )
    return RedirectResponse(url)

@router.get("/auth/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = await client.post(TOKEN_URL, data=data, headers=headers)
        token_response.raise_for_status()
        tokens = token_response.json()

        # Get user info
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        user_response = await client.get(USER_URL, headers=headers)
        user_response.raise_for_status()
        user = user_response.json()

    # You can create a session or JWT here, for now just return user info
    return JSONResponse(content=user)
