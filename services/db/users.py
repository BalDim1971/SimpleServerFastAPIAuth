"""
Сервисные функции по работе с базой данных для пользователей.
1. create_user - Создание пользователя.
2. get_user - Получение данных о пользователе по имени.
3. get_user_by_id - Получение данных о пользователе по id.
4. get_users - Получение данных о всех пользователях.
5. update_user - Обновление данных пользователя по id.
6. delete_user - Удаление пользователя по id.
"""

from sqlalchemy.orm import Session

from my_users.model import User
from my_users.schemas import CreateUserSchema, UserSchema, UserUpdateSchema


def create_user(session: Session, user: CreateUserSchema):
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(session: Session, username: str):
    return session.query(User).filter(User.username == username).one()


def get_user_by_id(session: Session, id: int):
    return session.query(User).filter(User.id == id).one()


def get_users(session: Session):
    return session.query(User).order_by(User.id)


def update_user(session: Session, id: int, user: UserUpdateSchema):
    db_user = session.query(User).filter(User.id == id).first()
    db_user.full_name = user.full_name
    db_user.is_active = user.is_active
    db_user.username = user.username
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, id: int):
    db_user = session.query(User).filter(User.id == id).first()
    session.delete(db_user)
    session.commit()
    return db_user
