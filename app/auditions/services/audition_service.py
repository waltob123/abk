import email_validator

from flask import Request
from app.auditions.models.models import Audition
from app.database.db_engine import session


class AuditionService:
    '''Class for audition services'''
    
    session = session()

    @classmethod
    def create_audition(cls, request: Request):
        '''Create audition'''
        data = request.get_json()

        try:
            email_validator.validate_email(data['email'])
        except (email_validator.EmailNotValidError, email_validator.EmailSyntaxError, email_validator.EmailUndeliverableError) as e:
            raise e
        
        audition = Audition(**data)
        cls.session.add(audition)
        try:
            cls.session.commit()
        except Exception as e:
            cls.session.rollback()
            cls.session.close()
            raise e
        return audition.to_dict()
