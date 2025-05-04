from pydantic import BaseModel, ConfigDict, field_validator
from user_management.common import exceptions as user_management_common_exceptions


class Base(BaseModel):


    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class Authentication(Base):


    email_or_username: str
    password: str


    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value):
        if value is not None and len(value) != 8:
            raise user_management_common_exceptions.InvalidPasswordLength
        return value