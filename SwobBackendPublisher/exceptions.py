class PlatformDoesNotExist(Exception):
    """PlatformDoesNotExist()

    Exception raised when Platform is not Found
    """

    def __init__(self, message="Platform Does Not Exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "Error: %s" % self.message

class UserDoesNotExist(Exception):
    """UserDoesNotExist()

    Exception raised when User is not Found
    """

    def __init__(self, message="User Does Not Exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "Error: %s" % self.message
        
class DuplicateUsersExist(Exception):
    """DuplicateUsersExist()

    Exception raised when Duplicate Users Exist
    """

    def __init__(self, message="Duplicate Users Exist"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "Error: %s" % self.message