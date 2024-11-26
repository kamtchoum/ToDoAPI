from fastapi import FastAPI
from dependancies.dependencies import engine
from sqlmodel import SQLModel
# from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.cors import CORSMiddleware
from endpoints.user import router as user_router
from endpoints.tasks import router as tasks_router
from endpoints.auth import router as auth_router


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(title="My To DO API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(tasks_router)


@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
