import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise
from .service import twitch, webhooks

load_dotenv('./server/.env')

app = FastAPI()
app.include_router(twitch.router)
app.include_router(webhooks.router)

origins = [
    "https://id.twitch.tv",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

register_tortoise(
    app,
    db_url=f"{os.getenv('DB_URL')}",
    modules={'models': ['server.model.user']},
    generate_schemas=True,
    add_exception_handlers=True,
)