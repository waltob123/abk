import jwt
from app.exceptions.token_exception import TokenExpiredException, TokenNotFoundException

class Token:
    '''Token class to generate and verify token'''

    @staticmethod
    def generate_token(payload, secret, algorithm='HS256'):
        '''Generate token'''
        return jwt.encode(payload, secret, algorithm=algorithm)

    @staticmethod
    def verify_token(token, secret, algorithm='HS256'):
        '''Verify token'''
        if token is None:
            raise TokenNotFoundException('Token is invalid.')
        try:
            payload = jwt.decode(token, secret, algorithms=[algorithm])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException('Token has expired.')
        except jwt.InvalidTokenError:
            raise TokenNotFoundException('Token is invalid.')
        
        return payload
