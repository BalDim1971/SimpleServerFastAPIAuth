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
        from_attributes = True


class UserLoginSchema(BaseModel):
    username: str = Field(alias="username")
    password: str


class UserUpdateSchema(UserBaseSchema):
    is_active: bool = Field(default=False)
