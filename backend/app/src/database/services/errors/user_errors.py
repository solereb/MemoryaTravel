class UserError(Exception):
    pass

class UserNotFoundError(UserError):
    pass

class UserServiceError(UserError):
    pass

class BadRegion(UserError):
    pass