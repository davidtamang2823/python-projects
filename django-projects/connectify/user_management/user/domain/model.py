from pydantic import BaseModel, ConfigDict, Field
from typing import NewType

UserId = NewType("UserId", int)

class Base(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )

class User(Base):
    id: UserId | None
    email: str | None
    password: str | None
    username: str | None
    first_name: str | None
    last_name: str | None
    is_active: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)
