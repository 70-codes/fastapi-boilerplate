from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services import create_db

app = FastAPI()
create_db()

origins = [
    "http://localhost:5173",
    "https://my-accountant.vercel.app",
    "http://localhost:3000",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
