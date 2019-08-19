# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class Pattern(Base):
    __tablename__ = 'patterns'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    template_id = Column(Integer, ForeignKey('templates.id'))
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    template = relationship("Template", backref=backref("patterns", cascade="all, delete-orphan", single_parent=True))

    # Relacion 1 a 1
    # diagram = relationship("Diagram", backref=backref("patterns", uselist=False, cascade="all, delete-orphan", single_parent=True))
    diagram = relationship("Diagram", backref=backref("patterns", cascade="all, delete-orphan", single_parent=True))
    scenario_components = relationship("ScenarioComponentPattern", back_populates="pattern", cascade="all, delete-orphan",
                                       single_parent=True)

    def __init__(self, name, template, diagram):
        self.name = name
        self.template = template
        self.diagram = diagram

    def __str__(self):
        cadena = '{}:{}'.format(self.id, self.name)
        return cadena
