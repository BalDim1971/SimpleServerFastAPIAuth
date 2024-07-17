from typing import Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.database import engine, create_db
from my_users.model import Base

from fastapi import Body, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from my_users import model as user_model
from my_users.schemas import CreateUserSchema, UserSchema, UserLoginSchema, UserUpdateSchema
from services.db import users as user_db_services

create_db()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Простой сервер с авторизацией",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post('/login', response_model=Dict)
def login(
    payload: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db)
):
    """
    Обрабатывает аутентификацию пользователя и возвращает токен
    при успешной аутентификации.
    Тело запроса:
    - имя пользователя: уникальный идентификатор пользователя, например:
     адрес электронной почты, имя
    - пароль:
    :return: str - токен пользователя
    """
    try:
        user: user_model.User = user_db_services.get_user(
            session=session, username=payload.username
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные пользователя"
        )
    
    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные пользователя"
        )
    
    return user.generate_token()


@app.post('/signup', response_model=UserSchema)
def signup(
    payload: CreateUserSchema = Body(),
    session: Session = Depends(get_db)
):
    """
    Обрабатывает запрос на регистрацию учетной записи пользователя.
    """
    payload.hashed_password = user_model.User.hash_password(
        payload.hashed_password)
    return user_db_services.create_user(session, user=payload)


@app.get("/profile/{id}", response_model=UserSchema)
def profile(
    id: int,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
):
    """
    Обрабатывает запрос на извлечение пользовательского
    профиля по идентификатору
    """
    try:
        user: user_model.User = user_db_services.get_user_by_id(
            session=session, id=id
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Пользователя с id = {id} нет."
        )
    return user_db_services.get_user_by_id(session=session, id=id)


@app.get("/users", response_model=List[UserSchema])
def get_users(session: Session = Depends(get_db)):
    """
    Запрос на получение списка всех пользователей.
    """
    return user_db_services.get_users(session=session)


@app.put("/profile/{id}", response_model=UserUpdateSchema)
def update_profile(
    id: int,
    payload: UserUpdateSchema = Body(),
    session: Session = Depends(get_db)
):
    """
    Обрабатываем запрос на обновление данных по пользователю.
    """
    try:
        user: user_model.User = user_db_services.get_user_by_id(
            session=session, id=id
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Пользователя с id = {id} нет."
        )
    return user_db_services.update_profile(session=session,
                                           id=id, user=payload)


if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(
        "main:app",
        log_level="info",
        reload=True)
