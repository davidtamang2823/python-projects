from events import Event

class SendUserVerificationEmail(Event):
    send_to: str
    send_to_username: str
    verification_token: str
