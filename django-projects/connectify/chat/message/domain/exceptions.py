class InvalidMessageLength(Exception):
    """Exception raised when the message length is invalid."""

    def __str__(self):
        return "Message length is invalid. It must be between 1 and 500 characters."