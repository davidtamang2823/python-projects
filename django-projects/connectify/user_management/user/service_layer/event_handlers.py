from events import message_bus
from user_management.user.common import constants
from user_management.user.domain import events as user_events
from user_management.tasks import send_verification_email_task

@message_bus.register_handler(event_type = constants.USER_REGISTRATION)
def handle_user_verification(event: user_events.SendUserVerificationEmail):
    send_verification_email_task.delay(event.send_to, event.send_to_username, event.verification_token)