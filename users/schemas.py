from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    username: str
    full_name: str


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool = Field(default=False)

    class Config:
        orm_mode = True
