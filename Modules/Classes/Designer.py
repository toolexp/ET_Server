# coding=utf-8

from sqlalchemy import Column, String, Integer
from Modules.Config.base import Base


class Designer(Base):
    __tablename__ = 'designers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def __str__(self):
        cadena = '{}:{}:{}'.format(self.id, self.name, self.surname)
        return cadena
