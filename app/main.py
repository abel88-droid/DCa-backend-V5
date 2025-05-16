# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import warnings
from app.auth import discord_oauth

app = FastAPI()

# CORS (frontend will talk to this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(discord_oauth.router)
app.include_router(warnings.router)

@app.get("/")
def home():
    return {"message": "Dashboard backend is live!"}
