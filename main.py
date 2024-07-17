from fastapi import FastAPI

from src.config import DB_HOST, DB_PORT
from src.database import engine, create_db
from users.model import Base

from fastapi import Body, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from users import model as user_model
from users.schemas import CreateUserSchema, UserSchema
from services.db import users as user_db_services

create_db()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Простой сервер с авторизацией",
)


# app.include_router(api_auth)
# app.include_router(api_users)


@app.post('/login')
async def login():
    """
    Обрабатывает аутентификацию пользователя и возвращает токен
    при успешной аутентификации.
    Тело запроса:
    - имя пользователя: уникальный идентификатор пользователя, например:
     адрес электронной почты, имя
    - пароль:
    :return: str - токен пользователя
    """
    return "ThisTokenIsFake"


@app.post('/signup', response_model=UserSchema)
def signup(
        payload: CreateUserSchema = Body(),
        session: Session = Depends(get_db)
):
    """Processes request to register user account."""
    payload.hashed_password = user_model.User.hash_password(
        payload.hashed_password)
    return user_db_services.create_user(session, user=payload)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        # host=DB_HOST,
        # port=int(DB_PORT),
        log_level="info",
        reload=True)
