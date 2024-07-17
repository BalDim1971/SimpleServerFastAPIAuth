from typing import List

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


def update_profile(session: Session, id: int, user: UserUpdateSchema):
    db_user = session.query(User).filter(User.id == id).first()
    db_user.full_name = user.full_name
    db_user.is_active = user.is_active
    db_user.username = user.username
    session.commit()
    session.refresh(db_user)
    return db_user
