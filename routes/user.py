from fastapi import Depends, status, HTTPException
from uuid import uuid4
from typing import List

from . import create_route
from schemas.user import UserCreate, UserShow, UserUpdate, ChangeUserPassword
from database import get_db
from models import User
from security.hash import Hash

from repository import user_repo

router = create_route(
    prefix="user",
    tags="User",
)


@router.post("/create", response_model=UserShow, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreate, db=Depends(get_db)):
    return await user_repo.create_user(
        db=db,
        request=request,
    )


@router.get("/all", response_model=List[UserShow])
async def get_all_users(db=Depends(get_db)):
    return await user_repo.get_all_users(db=db)


@router.get("/{user_id}", response_model=UserShow)
async def get_user_by_id(user_id: str, db=Depends(get_db)):
    return await user_repo.get_user_by_id(
        db=db,
        user_id=user_id,
    )


@router.patch("/{user_id}", response_model=UserShow)
async def update_user_details(
    user_id: str,
    request: UserUpdate,
    db=Depends(get_db),
):
    return await user_repo.update_user_details(
        db=db,
        user_id=user_id,
        request=request,
    )


@router.put("/{user_id}/change-password")
async def change_user_password(
    user_id: str,
    request: ChangeUserPassword,
    db=Depends(get_db),
):
    return await user_repo.change_user_password(
        db=db,
        user_id=user_id,
        request=request,
    )


@router.delete("/{user_id}")
async def delete_user(user_id: str, db=Depends(get_db)):
    return await user_repo.delete_user(
        db=db,
        user_id=user_id,
    )
