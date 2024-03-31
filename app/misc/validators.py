from app.exceptions.password_exception import PasswordTooShortException

class PasswordValidator:
    def __init__(self, password=None):
        self.password = password

    def validate(self):
        if len(self.password) < 8:
            raise PasswordTooShortException('Password must be at least 8 characters long.')
        return True
