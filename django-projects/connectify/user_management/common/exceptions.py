class InvalidPasswordLength(Exception):

    def __str__(self):
        return "Password Length Should Be Exactly 8."