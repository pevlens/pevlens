from sqlalchemy.exc import IntegrityError

class NotUniqvalue (IntegrityError):
    pass

class NulValue(Exception):
    pass