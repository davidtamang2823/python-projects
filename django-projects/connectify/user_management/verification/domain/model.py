from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator, Field
from user_management.verification.domain import exceptions as user_verification_exceptions
from user_management.common import exceptions as user_management_common_exceptions

class Base(BaseModel):


    model_config = ConfigDict(
        str_strip_whitespace=True
    )




class UserVerification(Base):


    token: str
    events: Optional[List] = Field(default_factory=list)

    @field_validator('token', mode='after')
    @classmethod
    def validate_username(cls, value):
        if value is not None and (len(value) != 64):
            raise user_verification_exceptions.InvalidToken
        return value
    

class PasswordReset(Base):


    token: str
    email: Optional[str] = None
    password: Optional[str] = None
    events: Optional[List] = Field(default_factory=list)

    @field_validator('password', mode='after')
    @classmethod
    def validate_password(cls, value):
        if value is not None and len(value) != 8:
            raise user_management_common_exceptions.InvalidPasswordLength
        return value


    @field_validator('token', mode='after')
    @classmethod
    def validate_username(cls, value):
        if value is not None and (len(value) != 64):
            raise user_verification_exceptions.InvalidToken
        return value