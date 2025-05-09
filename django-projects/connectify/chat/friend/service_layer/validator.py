from typing import Dict, Optional
from chat.friend.service_layer import exceptions as service_layer_exceptions


class UserFriendValidator:


    def validate_friend_request_not_accepted(self, status: str):
        if status == 'accepted':
            raise service_layer_exceptions.FriendRequestAccepted

    def validate_friend_request_not_pending(self, status: str):
        if status == 'pending':
            raise service_layer_exceptions.FriendRequestPending

    def validate_friend_exists_or_not(self, user_friend_details: Dict):
        if user_friend_details is None:
            raise service_layer_exceptions.FriendDoesNotExists
        
    def validate_can_send_request(self, current_status: Optional[str]):
        if current_status is None:
            return  # No existing record, can send request
        
        self.validate_friend_request_not_pending(current_status)
        self.validate_friend_request_not_accepted(current_status)