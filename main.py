from fastapi import FastAPI

from services import create_db

app = FastAPI()
create_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
