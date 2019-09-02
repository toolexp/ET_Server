# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class PatternSection(Base):
    __tablename__ = 'pattern_sections'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    pattern_id = Column(Integer, ForeignKey('patterns.id'))
    #template_section_id = Column(Integer, ForeignKey('templates_sections.id'))
    diagram_id = Column(Integer, ForeignKey('diagrams.id', use_alter=True, name='fk_pattern_sec_diagram_id'))
    pattern = relationship("Pattern", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                      single_parent=True))
    diagram = relationship("Diagram", foreign_keys=diagram_id, post_update=True, cascade="all, delete-orphan", single_parent=True)
    #template_section = relationship("TemplateSection", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                                        #single_parent=True))
    #diagram = relationship("Diagram", backref=backref("pattern_sections", cascade="all, delete-orphan", single_parent=True))

    # Relacion 1 a 1


    def __init__(self, content='', pattern=None, diagram=None):
        self.content = content
        self.pattern = pattern
        self.diagram = diagram

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}¥{}'.format(self.id, self.content, self.pattern.id, self.diagram.id)
        return cadena
