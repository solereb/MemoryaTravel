class AuthError(Exception):
    pass

class EmailAlreadyExistsError(AuthError):
    pass

class VerifyTokenExpiresError(AuthError):
    pass

class AccountNotFoundError(AuthError):
    pass

class IsAlreadyVerified(AuthError):
    pass

class DatabaseServiceError(AuthError):
    pass