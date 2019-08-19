# coding=utf-8

from sqlalchemy import Column, String, Integer, Boolean
from Modules.Config.base import Base


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    data_type = Column(String)
    mandatory = Column(Boolean)

    def __init__(self, name, description, data_type, mandatory):
        self.name = name
        self.description = description
        self.data_type = data_type
        self.mandatory = mandatory

    def __str__(self):
        if self.mandatory is True:
            aux = 'mandatory'
        else:
            aux = 'optional'
        cadena = '{}:{}:{}:{}:{}'.format(self.id, self.name, self.description, self.data_type, aux)
        return cadena
