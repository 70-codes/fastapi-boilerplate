from fastapi import HTTPException, status
from datetime import datetime
from uuid import uuid4

from models import User
from security.hash import Hash


async def get_user_by_username(db, username):
    user = db.query(User).filter(User.username == username).first()
    return user


async def get_user_by_email(db, email):
    user = db.query(User).filter(User.email == email).first()
    return user


async def get_all_users(db):
    users = db.query(User).all()
    return users


async def get_user_by_id(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def create_user(db, request):
    if await get_user_by_username(db=db, username=request.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    if await get_user_by_email(db=db, email=request.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    request.id = str(uuid4())
    request.password = Hash.get_password_hash(request.password)
    request.created_at = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    request.updated_at = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    new_user = User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user_details(db, user_id, request):
    user = await get_user_by_id(db=db, user_id=user_id)
    user.username = request.username if request.username else user.username
    user.fname = request.fname if request.fname else user.fname
    user.lname = request.lname if request.lname else user.lname
    user.email = user.email
    user.is_active = request.is_active if request.is_active else user.is_active
    user.is_superuser = (
        request.is_superuser if request.is_superuser else user.is_superuser
    )
    user.is_verified = request.is_verified if request.is_verified else user.is_verified
    user.updated_at = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.commit()
    db.refresh(user)
    return user


async def change_user_password(db, user_id, request):
    user = await get_user_by_id(db=db, user_id=user_id)
    if not Hash.verify_password(request.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )
    user.password = Hash.get_password_hash(request.new_password)
    user.updated_at = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.commit()
    db.refresh(user)
    return {
        "message": "Password changed succefully",
    }


async def delete_user(db, user_id):
    user = await get_user_by_id(db=db, user_id=user_id)
    db.delete(user)
    db.commit()
    return {
        "message": "User deleted successfully",
    }
