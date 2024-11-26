from sqlmodel import Field, SQLModel
from enum import Enum
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str
    full_name: EmailStr
    email: str
    phone_number: int


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    full_name: str | None = None
    phone_number: int | None = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr= Field(index=True, unique=True)
    password: str
    is_admin: bool | None = False


class TaksStatus(str, Enum):
    running = "running"
    finish = "finish"


class ToDoBase(SQLModel):
    title: str
    description: str
    status: TaksStatus


class ToDoPublic(ToDoBase):
    id: int
    user_id: int


class ToDoCreate(ToDoBase):
    pass


class ToDoUpdate(SQLModel):
    title: str | None = None
    description: str | None = None


class ToDo(ToDoBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
