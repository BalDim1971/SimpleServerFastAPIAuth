from sqlalchemy.orm import Session
from sqlalchemy import select

from users.model import User
from users.schemas import CreateUserSchema


def create_user(session: Session, user: CreateUserSchema):
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
