class FriendRequestPending(Exception):


    def __str__(self):
        return 'Friend request already sent.'
    

class FriendRequestAccepted(Exception):


    def __str__(self):
        return 'You are already friend with this user.'
    

class FriendDoesNotExists(Exception):


    def __str__(self):
        return 'Friendship does not exists.'