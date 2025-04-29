from events import Event

class ResendUserVerificationEmail(Event):
    send_to: str
    send_to_username: str
    verification_token: str


class SendPasswordResetEmail(Event):
    send_to: str
    send_to_username: str
    verification_token: str