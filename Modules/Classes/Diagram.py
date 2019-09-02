# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, backref

from Modules.Config.base import Base


class Diagram(Base):
    __tablename__ = 'diagrams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_path = Column(String)
    #pattern_sec = relationship("PatternSection", backref=backref("diagram", uselist=False, cascade="all, delete-orphan"))

    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path

    def __str__(self):
        cadena = '{}¥{}'.format(self.name, self.file_path)
        return cadena
