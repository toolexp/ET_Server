# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class PatternSection(Base):
    __tablename__ = 'pattern_sections'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    pattern_id = Column(Integer, ForeignKey('patterns.id'))
    section_id = Column(Integer, ForeignKey('sections.id'))
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    pattern = relationship("Pattern", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                      single_parent=True))
    section = relationship("Section", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                      single_parent=True))
    diagram = relationship("Diagram", backref=backref("pattern_sections", cascade="all, delete-orphan", single_parent=True))

    # Relacion 1 a 1
    # diagram = relationship("Diagram", backref=backref("patterns", uselist=False, cascade="all, delete-orphan", single_parent=True))

    def __init__(self, content='', pattern=None, section=None, diagram=None):
        self.content = content
        self.pattern = pattern
        self.section = section
        self.diagram = diagram

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}¥{}'.format(self.id, self.content, self.pattern, self.section, self.diagram)
        return cadena
