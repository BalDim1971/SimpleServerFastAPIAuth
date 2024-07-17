from typing import Dict, Any

import jwt
from sqlalchemy import (
    LargeBinary,
    Column,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    PrimaryKeyConstraint
)
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

from src.config import JWT_SECRET_KEY

Base = declarative_base()


class User(Base):
    """Models a user table"""
    __tablename__ = "my_users"
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(225), nullable=False, unique=True)
    hashed_password = Column(LargeBinary, nullable=False)
    full_name = Column(String(225), nullable=False)
    is_active = Column(Boolean, default=False)

    UniqueConstraint("username", name="uq_user_name")
    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self):
        """Возвращает строковое представление экземпляра модели"""
        return "<User {full_name!r}>".format(full_name=self.full_name)

    @staticmethod
    def hash_password(password) -> bytes:
        """
        Преобразует пароль из его необработанной текстовой формы в
        криптографические хэши
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> dict[str, Any]:
        """Confirms password validity"""
        return {
            "access_token": jwt.encode(
                {"full_name": self.full_name, "username": self.username},
                "ApplicationSecretKey"
            )
        }

    def generate_token(self) -> dict:
        """Generate access token for user"""
        return {
            "access_token": jwt.encode(
                {"full_name": self.full_name, "username": self.username},
                JWT_SECRET_KEY
            )
        }