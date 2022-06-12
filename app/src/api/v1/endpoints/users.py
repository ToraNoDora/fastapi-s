from typing import Any, List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from src.core.jwt import get_current_user
from src.redis.cache import RedisCache
from src.store.db import get_store
from src.store.models.users import User
from src.crud.users import UserCrud
from src.crud.validator import verify_email_exist
from src.schemas.users import UserBase, UserCreate, UserUpdate, DisplayUser, UserStore


router = APIRouter()
user_crud = UserCrud(User)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: UserCreate, db: Session=Depends(get_store)):
    """New user registration"""
    user = await verify_email_exist(request.email, db)

    if user:
        raise HTTPException(
            status_code = 400,
            detail = "The user with this email already exists in the system"
        )

    new_user = await user_crud.create(db=db, obj_in=request)

    async with RedisCache() as cache:
        await cache.delete("all users")

    return new_user


@router.get("/{user_id}", response_model=DisplayUser)
async def get_user(user_id: int, db: Session = Depends(get_store), current_user: UserBase = Depends(get_current_user)) -> Any:
    """Fetch a single user by id"""
    user = await user_crud.get(db=db, id=user_id)

    cache_key = f"user {user_id}"

    async with RedisCache() as cache:
        user_cache = await cache.get(cache_key)

        if user_cache:
            return user_cache

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found..",
        )

    async with RedisCache() as cache:
        await cache.set(cache_key, user)

    return user


@router.put("/{user_id}", status_code=status.HTTP_201_CREATED, response_model=UserStore)
async def update_user(user_id: int, *, user_in: UserUpdate, db: Session = Depends(get_store), current_user: User = Depends(get_current_user)) -> Any:
    """Update user in the store"""
    user = await user_crud.get(db=db, id=user_id)
    updated_user = await user_crud.update(db=db, current_email=current_user.email, db_obj=user, obj_in=user_in)

    async with RedisCache() as cache:
        await cache.delete(f"user {user_id}")
        await cache.delete("all users")

    return updated_user


@router.get("/", response_model=List[DisplayUser])
async def get_users(db: Session = Depends(get_store), current_user: UserBase = Depends(get_current_user)):
    """Fetch all users"""
    cache_key = f"all users"

    async with RedisCache() as cache:
        users_cache = await cache.get(cache_key)

        if users_cache:
            return users_cache

    users = await user_crud.get_all(db=db)


    async with RedisCache() as cache:
        await cache.set_multi(cache_key, users)

    return users


@router.delete("/{user_id}",  status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user(user_id: int, db: Session = Depends(get_store), current_user: UserBase = Depends(get_current_user)):
    """Delete a single user by id"""
    result = await user_crud.delete(db=db, id=user_id)

    return result


