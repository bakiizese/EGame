#!/usr/bin/python3
''' user managment '''
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash
import uuid

hostname = 'bekii.mysql.pythonanywhere-services.com'
username = 'bekii'
password = 'alxmysql'
database_name = 'bekii$default'
connection_string = f"mysql+pymysql://{username}:\
                     {password}@{hostname}/{database_name}"
mysql = 'mysql+pymysql://Chatdb:chatdb_pwd@localhost/realtime_db'

engine = create_engine(mysql)
Base = declarative_base()


class User(Base):
    '''a Class for create and retriev user'''
    __tablename__ = 'users'
    id = Column(String(60), primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(128), nullable=False)
    password = Column(String(256), nullable=False)
    

    def __init__(self, id, username, email, password):
        '''signing id, name, email and password of a new user'''
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def is_authenticated():
        '''returns true if a user is authenticated'''
        return True

    @staticmethod
    def is_active():
        '''returns true if a user is active'''
        return True

    @staticmethod
    def is_anonymous():
        '''returns true if a user is anonymous'''
        return False

    def get_id(self):
        '''returns username from db'''
        return self.username

    def check_password(self, password_input):
        '''returns true if password is correct'''
        return check_password_hash(self.password, password_input)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
