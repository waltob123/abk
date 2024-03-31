from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, String, Enum, Integer, Text, CheckConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from .base_model import BaseModel, Base


class Audition(Base, BaseModel):
    '''Audition model for all models in the app.'''

    __tablename__ = 'auditions'

    fullname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(10), nullable=False)
    area = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    country = Column(String(255), nullable=True)
    category = Column(Enum(*('Individual', 'Group')), nullable=False, default='Individual')
    video_link = Column(String(255), nullable=False)
    stage_name = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)
    team_name = Column(String(255), nullable=True)
    age_range = Column(String(255), nullable=True)
    team_size = Column(Integer, nullable=True)
    description = Column(Text, nullable=False)
    __table_args__ = (
        CheckConstraint('team_size >= 12 AND team_size <= 15'),
    )

    def __init__(self, fullname, email, phone, area, city, category, description, video_link,
                 country=None, team_name=None, age_range=None, team_size=None, stage_name=None, age=None):
        '''Initialize audition model.'''
        self.fullname = fullname
        self.email = email
        self.phone = phone
        self.area = area
        self.city = city
        self.country = country
        self.category = category
        self.video_link = video_link
        self.description = description
        if self.category == 'Group':
            self.team_name = team_name
            self.age_range = age_range
            self.team_size = team_size
        elif self.category == 'Individual':
            self.stage_name = stage_name
            self.age = age

    def to_dict(self):
        '''Return dictionary representation of audition model.'''
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'phone': self.phone,
            'area': self.area,
            'city': self.city,
            'country': self.country,
            'category': self.category,
            'video_link': self.video_link,
            'stage_name': self.stage_name,
            'age': self.age,
            'team_name': self.team_name,
            'age_range': self.age_range,
            'team_size': self.team_size,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __str__(self):
        '''String representation of audition model.'''
        return f'<{self.__class__.__name__} {self.id}>'

    def __repr__(self):
        '''String representation of audition model.'''
        return f'{self.__class__.__name__}()'


class User(Base, UserMixin, BaseModel):
    '''User model for all models in the app.'''

    __tablename__ = 'users'

    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_validated = Column(Boolean, default=False)
    __table_args__ = (
        CheckConstraint('LENGTH(password) >= 8'),
    )

    def __init__(self, email: str, password: str, is_validated=False):
        '''Initialize user model.'''
        self.email = email
        self.password = password
        self.is_validated = is_validated

    def to_dict(self):
        '''Return dictionary representation of user model.'''
        return {
            'id': self.id,
            'email': self.email,
            'is_validated': self.is_validated,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __str__(self):
        '''String representation of user model.'''
        return f'<{self.__class__.__name__} {self.id}>'

    def __repr__(self):
        '''String representation of user model.'''
        return f'{self.__class__.__name__}(\'{self.email}\', \'{self.password}\')'
