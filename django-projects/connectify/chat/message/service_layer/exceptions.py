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