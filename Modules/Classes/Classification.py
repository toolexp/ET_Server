# coding=utf-8

from sqlalchemy import Column, String, Integer

from Modules.Config.base import Base


class Classification(Base):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.name, len(self.categories))
        return cadena
