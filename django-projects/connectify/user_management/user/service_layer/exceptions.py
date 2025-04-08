class EmailAlreadyExists(Exception):


    def __str__(self):
        return "Email Already Exists."
    

class UserNameAlreadyExists(Exception):


    def __str__(self):
        return "Username Already Exists."
    
class UserNotFound(Exception):

    def __str__(self):
        return "User Does Not Exists."