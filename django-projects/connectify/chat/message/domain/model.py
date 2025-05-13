from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
from chat.message.domain import exceptions as domain_layer_exceptions

class Base(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class PrivateChatModel(BaseModel):


    sender_id: int
    receiver_id: int
    content: str
    id: Optional[int] = None
    is_seen: Optional[bool] = False

    @field_validator('content', mode='after')
    @classmethod
    def validate_content(cls, value):
        if not value or len(value) > 20000:
            raise domain_layer_exceptions.InvalidMessageLength
        return value
    
