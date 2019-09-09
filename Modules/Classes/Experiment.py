# coding=utf-8

from sqlalchemy import Column, String, Integer
from Modules.Config.base import Base


class Experiment(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.name, self.description)
        return cadena
