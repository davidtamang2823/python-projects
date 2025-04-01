from events import Event

class SendUserRegistrationConfirmationEmail(Event):
    send_to: str
    verification_code: int
