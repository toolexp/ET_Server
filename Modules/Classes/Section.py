# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from Modules.Config.base import Base


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    data_type = Column(String)

    def __init__(self, name, description, data_type):
        self.name = name
        self.description = description
        self.data_type = data_type

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.data_type)
        return cadena
