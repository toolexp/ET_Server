# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class Pattern(Base):
    __tablename__ = 'patterns'

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('templates.id'))

    template = relationship("Template", backref=backref("patterns", cascade="all, delete-orphan", single_parent=True))

    def __init__(self,template):
        self.template = template

    def __str__(self):
        cadena = '{}¥{}'.format(self.id, self.template_id)
        return cadena
