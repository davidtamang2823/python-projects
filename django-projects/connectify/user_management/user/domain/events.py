from events import Event

class SendUserRegistrationConfirmationEmail(Event):
    send_by: str
    send_to: str
    subject: str
    verification_code: int
