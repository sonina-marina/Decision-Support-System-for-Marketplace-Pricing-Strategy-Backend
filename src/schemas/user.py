from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class UserBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True
    )


class UserCreate(UserBaseModel):
    email: EmailStr
    fullname: str
    password: str


class UserView(UserBaseModel):
    id: int
    email: EmailStr
    fullname: str


class UserList(UserBaseModel):
    count: int
    items: list[UserView]


class UserUpdatePassword(UserBaseModel):
    id: int
    new_password: str


class UserUpdateFullname(UserBaseModel):
    id: int
    new_fullname: str
