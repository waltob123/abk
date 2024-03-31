import os
import email_validator
import bcrypt
from flask import Request
from flask_login import login_user, logout_user, current_user
from http import HTTPStatus
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app import login_manager
from app.database.db_engine import session
from app.auditions.models.models import User
from app.exceptions.password_exception import PasswordTooShortException, PasswordNotMatchException
from app.exceptions.duplicate_exception import DuplicateException
from app.exceptions.user_exception import UserNotFoundException
from app.misc.token import Token
from app.misc.mailer import Mailer


from app.misc.validators import PasswordValidator


class AuthService:
    '''Authentication service.'''
    
    new_session = session()
    token = Token()
    mailer = Mailer()
    
    @login_manager.user_loader
    @classmethod
    def load_user(cls, user_id):
        '''Load user.'''
        user = cls.new_session.query(User).filter_by(id=user_id).first()
        cls.new_session.close()
        return user
    
    @classmethod
    def register(cls, request: Request):
        '''Regsiter user'''
        
        data = request.get_json()
        
        # validate email
        try:
            email_validator.validate_email(data['email'])
        except (email_validator.EmailNotValidError, email_validator.EmailSyntaxError, email_validator.EmailUndeliverableError) as e:
            raise e

        # Validate password
        try:
            password_validator = PasswordValidator(data['password'])
            password_validator.validate()
        except PasswordTooShortException as e:
            raise e
        
        # hash password
        data['password'] = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = User(**data)  # Create user object
        cls.new_session.add(user)  # Add user to session
        
        # Commit the session
        try:
            cls.new_session.commit()
        except IntegrityError as e:
            cls.new_session.rollback()
            cls.new_session.close()
            raise DuplicateException('User already exists.')
        
        payload = {'email': user.email, 'exp': datetime.utcnow() + timedelta(days=1)}
        new_token = cls.token.generate_token(payload=payload, secret=os.getenv('SECRET_KEY'))
        link = request.host_url + f'auth/verify?token={new_token}'
        cls.mailer.send_email(
            subject='Account Verification', 
            email=user.email, 
            sender=os.environ.get('MAIL_USERNAME'),
            msg=f'Click on {link} to verify your account.'
            )
        return user.to_dict()

    @classmethod
    def verify_account(cls, request: Request):
        user_token = request.args.get('token')

        try:
            payload = cls.token.verify_token(token=user_token, secret=os.environ.get('SECRET_KEY'))
        except Exception as e:
            raise e

        user = cls.new_session.query(User).filter_by(email=payload.get('email')).first()
        
        if not user:
            cls.new_session.close()
            raise UserNotFoundException('User not found!')

        user.is_validated = True
        cls.new_session.commit()
        return user.to_dict()

    @classmethod
    def login(cls, request: Request):
        '''Login user.'''
        data = request.get_json()
        user = cls.new_session.query(User).filter_by(email=data['email']).first()
        cls.new_session.close()
        
        if not user:
            raise UserNotFoundException('User not found.')
        
        if not user.is_validated:
            raise UserNotFoundException('User not validated.')
        
        if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
            raise PasswordNotMatchException('Password does not match.')
        
        login_user(user)
        return user.to_dict()
