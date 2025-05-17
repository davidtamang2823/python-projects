class UserNotFriendError(Exception):


    def __str__(self):
        return "You are not a friend with this user. Cannot send message."
    

class UserBlocked(Exception):


    def __str__(self):
        return "You are blocked by this user. Cannot send message."
    

class UserFriendRequestPending(Exception):


    def __str__(self):
        return "You have a pending friend request with this user. Cannot send message."
    

class UserFriendRequestRejected(Exception):


    def __str__(self):
        return "You have a rejected friend request with this user. Cannot send message."
    
class UserNotSender(Exception):


    """
    Exception raised when the user is not the sender of the message.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class MessageNotFound(Exception):

    def __str__(self):
        return "Message not found."