from events import Event

class SendUserRegistrationConfirmationEmail(Event):
    send_to: str
    send_to_username: str
    verification_token: str
