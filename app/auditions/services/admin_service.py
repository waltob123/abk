from flask import Request
from flask_login import current_user, login_required
from app.auditions.models.models import Audition
from app.database.db_engine import session


class AdminService:
    '''Admin Service'''

    session = session()
    
    # @classmethod
    @login_required
    def get_all_auditions(self):
        '''Get all auditions'''
        auditions = self.session.query(Audition).all()
        return [audition.to_dict() for audition in auditions]

    # @classmethod
    @login_required
    def get_audition(self, audition_id):
        '''Get audition'''
        audition = self.session.query(Audition).filter_by(id=audition_id).first()
        return audition.to_dict()
