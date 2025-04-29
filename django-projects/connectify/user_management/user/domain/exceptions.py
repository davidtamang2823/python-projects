
class InvalidUserFullNameLength(Exception):


    def __str__(self):
        return "First Name or Last Name Length Should Be Between 3 And 150."
    

class InvalidUserNameLength(Exception):


    def __str__(self):
        return "Username Length Should Be Between 6 Or 150 Character."
    

class InvalidEmailLength(Exception):


    def __str__(self):
        return "Email Length Should Be Between 3 Or 254 Character."