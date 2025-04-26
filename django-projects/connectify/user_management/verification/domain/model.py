from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator, Field
from user_management.verification.domain import exceptions as user_verification_exceptions

class Base(BaseModel):


    model_config = ConfigDict(
        str_strip_whitespace=True
    )




class UserVerification(BaseModel):


    token: str
    events: Optional[List] = Field(default_factory=list)

    @field_validator('token', mode='after')
    @classmethod
    def validate_username(cls, value):
        if value is not None and (len(value) != 64):
            raise user_verification_exceptions.InvalidToken
        return value