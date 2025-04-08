from events import message_bus
from user_management.user.common import constants
from user_management.user.domain import events as user_events
from user_management.tasks import send_user_confirmation_email

@message_bus.register_handler(event_type = constants.USER_REGISTRATION)
def handle_user_registration_confirmation(event: user_events.SendUserRegistrationConfirmationEmail):
    send_user_confirmation_email.delay(event.send_to, event.send_to_username, event.verification_token)