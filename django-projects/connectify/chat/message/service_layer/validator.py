from typing import Dict
from chat.message.service_layer import exceptions as service_layer_exceptions


class PrivateChatValidator:


    def validate_receiver_is_friend_or_not(self, user_friend_details: Dict):
        if user_friend_details is None:
            raise service_layer_exceptions.UserNotFriendError


    def validate_send_message_eligibility(self, status: str):
        if status == 'blocked':
            raise service_layer_exceptions.UserBlocked
        elif status == 'pending':
            raise service_layer_exceptions.UserFriendRequestPending
        elif status == 'rejected':
            raise service_layer_exceptions.UserFriendRequestRejected
        

    def validate_can_update_message(self, sender_id: int, existing_sender_id: int):
        if sender_id != existing_sender_id:
            raise service_layer_exceptions.UserNotSender("You are not the sender of this message. Cannot update message.")

    def validate_can_delete_message(self, sender_id: int, existing_sender_id: int):
        if int(sender_id) != existing_sender_id:
            raise service_layer_exceptions.UserNotSender('Cannot delete message. You are not the sender of this message.')

    def validate_message_existence(self, message_details: Dict):
        if message_details is None:
            raise service_layer_exceptions.MessageNotFound