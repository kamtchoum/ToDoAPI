from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from dependancies.dependencies import SessionDep
from models.models import User, UserCreate, UserPublic, UserUpdate
from security.security import (
    get_current_user,
    get_password_hash,
    get_admin_user,
)

router = APIRouter()


@router.delete("/users/{id}", tags=["Admin"])
def delete_user(
    id: int,
    session: SessionDep,
    current_admin_user: Annotated[User, Depends(get_admin_user)],
):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"Supression": True}


@router.get("/users/me", response_model=UserPublic, tags=["Users"])
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.get(
    "/users/{id}", response_model=UserPublic, tags=["Admin"]
)
def read_user(
    id: int,
    session: SessionDep,
    current_admin_user: Annotated[User, Depends(get_admin_user)],
):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=list[UserPublic], tags=["Admin"])
def read_users(
    session: SessionDep,
    current_admin_user: Annotated[User, Depends(get_admin_user)],
):
    user = session.exec(select(User)).all()
    return user


@router.post("/users/", response_model=UserPublic, tags=["Users"])
def create_user(user: UserCreate, session: SessionDep) -> User:
    user.password = get_password_hash(user.password)
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch(
    "/users/{username}", response_model=UserPublic, tags=["Users"]
)
def update_user(username: str, user: UserUpdate, session: SessionDep):
    user_db = session.exec(select(User).where(User.username == username))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    # user_data = user.model_dump(exclude_unset=True)

    user_data = user.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(user_db, key, value)
    user_db = user_data
    # user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db
