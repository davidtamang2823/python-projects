from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import NewType, List, Optional

from events import Event
from user_management.user.domain import exceptions as user_domain_exceptions
from user_management.common import exceptions as user_management_common_exceptions

UserId = NewType("UserId", int)

class Base(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )

class User(Base):


    id: Optional[UserId] = None
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = False
    events: List[Event] = Field(default_factory=list)

    @field_validator('first_name', 'last_name', mode='after')
    @classmethod
    def validate_name(cls, value):
        if value is not None and (len(value) > 150 or len(value) < 3):
            raise user_domain_exceptions.InvalidUserFullNameLength
        return value

    @field_validator('username', mode='after')
    @classmethod
    def validate_username(cls, value):
        if value is not None and (len(value) > 150 or len(value) < 6):
            raise user_domain_exceptions.InvalidUserNameLength
        return value

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value):
        if value is not None and len(value) != 8:
            raise user_management_common_exceptions.InvalidPasswordLength
        return value

    @field_validator('email', mode="after")
    @classmethod
    def validate_email(cls, value):
        if value is not None and (len(value) < 3 or len(value) > 254):
            raise user_domain_exceptions.InvalidEmailLength
        return value