from fastapi import Depends
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer

from . import create_route
from database import get_db
from schemas.user import UserLogin
from schemas.token import Token
from repository import token_repo


router = create_route(
    prefix="auth",
    tags="Auth",
)

auth_dep = AuthJWTBearer()


@router.post("/login", response_model=Token)
async def login(
    request: UserLogin,
    auth: AuthJWT = Depends(),
    db=Depends(get_db),
):
    return await token_repo.create_token(
        request=request,
        auth=auth,
        db=db,
    )


@router.post("/refresh")
async def refresh(authorize: AuthJWT = Depends(auth_dep)):
    await authorize.jwt_refresh_token_required()
    current_user = await authorize.get_jwt_subject()
    new_access_token = await authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
