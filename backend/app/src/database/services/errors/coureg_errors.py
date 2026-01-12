class CouRegError(Exception):
    pass

class NotFoundCouReg(CouRegError):
    pass

class CouRegServiceError(CouRegError):
    pass