class SameUserFriendId(Exception):


    def __str__(self):
        return 'Current logged in user id and friend id should not be same.'
