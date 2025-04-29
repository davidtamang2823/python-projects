class TokenExpired(Exception):


    def __str__(self):
        return "Your token has been expired. Please request again."


class TokenNotFound(Exception):


    def __str__(self):
        return "Token not found."
    

class UserAlreadyVerified(Exception):


    def __str__(self):
        return "User already verified."
    

class UnregisteredUser(Exception):


    def __str__(self):
        return "User Not Found."
    

class TokenNotExpired(Exception):


    def __str__(self):
        return "Token not expired."
    

class UserAlreadyVerified(Exception):


    def __str__(self):
        return "User has been verified already."