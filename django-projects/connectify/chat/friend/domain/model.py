from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator
from chat.friend.domain import exceptions as domain_layer_exceptions

class Base(BaseModel):


    model_config = ConfigDict(
        str_strip_whitespace=True
    )


class UserFriendStatus(str, Enum):


    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'
    blocked = 'blocked'


class UserFriend(BaseModel):


    user_id: int
    friend_id: int
    status: UserFriendStatus = Field(default=UserFriendStatus.pending)


    @model_validator(mode='after')
    def validate_user_friend(self):
        if self.user_id == self.friend_id and self.status == UserFriendStatus.pending:
            raise domain_layer_exceptions.SameUserFriendId
        return self
