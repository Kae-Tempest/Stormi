from fastapi import FastAPI
from tortoise import run_async
from server.database.connection import init
from fastapi.middleware.cors import CORSMiddleware

run_async(init())
app = FastAPI()

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
