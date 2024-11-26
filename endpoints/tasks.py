# from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from dependancies.dependencies import SessionDep
from models.models import (
    # TaksStatus,
    ToDo,
    ToDoCreate,
    ToDoPublic,
    # ToDoUpdate,
    User,
)
from security.security import (
    # ACCESS_TOKEN_EXPIRE_MINUTES,
    # Token,
    # authenticate_user,
    # create_access_token,
    get_current_user,
    # timedelta,
)

router = APIRouter(tags=["Tasks"])


# adding of one task
@router.post("/tasks/", response_model=ToDoPublic)
def create_task(
    todo: ToDoCreate,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> ToDo:
    todo_db = ToDo(
        title=todo.title,
        description=todo.description,
        status=todo.status,
        user_id=current_user.id,
    )
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db


@router.get("/tasks/", response_model=list[ToDoPublic])
def read_tasks(
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[ToDoPublic]:
    tasks = session.exec(select(ToDo)).all()
    tasks_user = []
    for task in tasks:
        if task.user_id == current_user.id:
            tasks_user.append(task)
    return tasks_user


@router.get("/tasks/{id}", response_model=ToDoPublic)
def read_task(
    id: str,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
) -> ToDoPublic:
    todo = session.exec(
        select(ToDo).where(
            ToDo.id == id, ToDo.user_id == current_user.id
        )
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Taks not found")
    return todo


@router.delete("/task/{id}")
def delete_taks(
    id: int,
    session: SessionDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    todo = session.exec(select(ToDo).where(ToDo.id == id)).first()

    if not todo:
        raise HTTPException(status_code=404, detail="task not found")
    if not todo.user_id == current_user.id:
        raise HTTPException(
            status_code=404, detail="Sorry you can not delete this task"
        )

    session.delete(todo)
    session.commit()
    return {"Task deleted": True}


# @router.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
#     session: SessionDep,
# ) -> Token:
#     user = authenticate_user(form_data.username, form_data.password, session)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return Token(access_token=access_token, token_type="bearer")


# @router.patch("/tasks/{task_title}/status", response_model=ToDoPublic)
# def update_task_status(
#     task_title: str,
#     task: TaksStatus,
#     session: SessionDep,
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     task_db = session.exec(select(ToDo).where(ToDo.title == task_title))
#     if not task_db:
#         raise HTTPException(status_code=404, detail="task not found")
#     if not task_db.user_id == current_user.id:
#         raise HTTPException(
#             status_code=404,
#             detail="Sorry you can't update the status of this task",
#         )
#     task_db.status = task
#     session.add(task_db)
#     session.commit()
#     session.refresh(task_db)
#     return task_db


# @router.patch("/tasks/{task_title}/status", response_model=ToDoPublic)
# def update_task(
#     task_title: str,
#     task: ToDoUpdate,
#     session: SessionDep,
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     task_db = session.exec(select(ToDo).where(ToDo.title == task_title))
#     if not task_db:
#         raise HTTPException(status_code=404, detail="task not found")
#     if not task_db.user_id == current_user.id:
#         raise HTTPException(
#             status_code=404, detail="Sorry you can't update this task"
#         )
#     task_data = task.model_dump(exclude_unset=True)
#     task_db.title = task_data.title
#     task_db.description = task_data.description
#     session.add(task_db)
#     session.commit()
#     session.refresh(task_db)
#     return task_db
