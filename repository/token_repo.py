from fastapi import HTTPException, status
from datetime import timedelta


from models import User
from security.hash import Hash
from repository import user_repo


async def create_token(request, auth, db):
    user = await user_repo.get_user_by_username(db=db, username=request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username or password",
        )
    if not Hash.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username or password",
        )
    expiration_time = 20
    expires = timedelta(minutes=expiration_time)

    access_token = await auth.create_access_token(subject=user.id, expires_time=expires)
    refresh_token = await auth.create_refresh_token(subject=user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_token_expiration_time": expiration_time,
    }
