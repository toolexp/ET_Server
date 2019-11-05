# coding=utf-8

from sqlalchemy import Column, Integer, String
from Modules.Config.base import Base


class Metric(Base):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.name, self.description)
        return cadena
