from events import message_bus
from user_management.verification.common import constants
from user_management.verification.domain import events as user_verification_events
from user_management.tasks import send_verification_email_task, send_password_reset_email_task

@message_bus.register_handler(event_type = constants.RESEND_VERIFICATION_EMAIL)
def handle_resend_user_verification(event: user_verification_events.ResendUserVerificationEmail):
    send_verification_email_task.delay(event.send_to, event.send_to_username, event.verification_token)

@message_bus.register_handler(event_type = constants.SEND_PASSWORD_RESET_EMAIL)
def handle_send_password_reset_email(event: user_verification_events.SendPasswordResetEmail):
    send_password_reset_email_task.delay(event.send_to, event.send_to_username, event.verification_token)