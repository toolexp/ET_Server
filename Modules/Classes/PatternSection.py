# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class PatternSection(Base):
    __tablename__ = 'pattern_sections'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    pattern_id = Column(Integer, ForeignKey('patterns.id'))
    pattern = relationship("Pattern", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                      single_parent=True))

    def __init__(self, content, pattern):
        self.content = content
        self.pattern = pattern

    def __str__(self):
        cadena = '{}:{}'.format(self.id, self.content)
        return cadena
