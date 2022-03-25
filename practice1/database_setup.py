from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    token = Column(String(36), nullable=False)


class Notebook(Base):
    __tablename__ = 'notebook'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=True)
    text = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(250), nullable=True)
    bot_answer = Column(String(250), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))


engine = create_engine('postgresql+psycopg2://wad-adm:StrongPassw0rd@127.0.0.1:55437/wad_db')
Base.metadata.create_all(engine)
