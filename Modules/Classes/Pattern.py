# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class Pattern(Base):
    __tablename__ = 'patterns'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    template_id = Column(Integer, ForeignKey('templates.id'))
    template = relationship("Template", backref=backref("patterns", cascade="all, delete-orphan", single_parent=True))
    scenario_components = relationship("ScenarioComponentPattern", back_populates="pattern", cascade="all, delete-orphan",
                                       single_parent=True)

    def __init__(self, name, template):
        self.name = name
        self.template = template

    def __str__(self):
        cadena = '{}¥{}'.format(self.id, self.name)
        return cadena
