from fastapi import FastAPI

from src.config import DB_HOST, DB_PORT
from src.database import engine, create_db
from users.model import Base

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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        # host=DB_HOST,
        # port=int(DB_PORT),
        log_level="info",
        reload=True)
