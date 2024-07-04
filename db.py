#!/usr/bin/python3
'''reloading and creating user db using mysql'''
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import sqlalchemy
from user import User
from werkzeug.security import check_password_hash, generate_password_hash

hostname = 'Bereketzeselassie.mysql.pythonanywhere-services.com'
username = 'Bereketzeselassi'
password = 'alxmysql'
database_name = 'Bereketzeselassi$realtime_db'

connection_string = f"mysql+pymysql://{username}:\
                     {password}@{hostname}/{database_name}"

mysql = 'mysql+pymysql://Chatdb:chatdb_pwd@localhost/realtime_db'

engine = create_engine(mysql)
Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Chatdbs:
    '''Mysql Database'''
    @staticmethod
    def new(username, email, password):
        '''to register a new user in the db'''
        hpassword = generate_password_hash(password)
        add = User(id='10', username=username, email=email, password=hpassword)
        session = Session()
        session.add(add)
        session.commit()


    def get_user(username):
        '''to retriev a user form a db'''
        session = Session()
        return session.query(User).filter_by(username=username).first()
