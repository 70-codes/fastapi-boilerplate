from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from async_fastapi_jwt_auth import AuthJWT
from schemas.token import Settings

from services import create_db

from routes import user

app = FastAPI()
create_db()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


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


app.include_router(user.router)
