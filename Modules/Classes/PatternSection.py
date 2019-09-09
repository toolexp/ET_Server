# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class PatternSection(Base):
    __tablename__ = 'pattern_sections'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    pattern_id = Column(Integer, ForeignKey('patterns.id'))
    temp_section_id = Column(Integer, ForeignKey('templates_sections.id'))
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    pattern = relationship("Pattern", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                      single_parent=True))
    temp_section = relationship("TemplateSection", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                                   single_parent=True))
    diagram = relationship("Diagram", foreign_keys=diagram_id, post_update=True, cascade="all, delete-orphan",
                           single_parent=True)
    category = relationship("Category", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                        single_parent=True))

    def __init__(self, content='', pattern=None, temp_section=None, diagram=None, category=None):
        self.content = content
        self.pattern = pattern
        self.temp_section = temp_section
        self.diagram = diagram
        self.category = category

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}¥{}¥{}'.format(self.id, self.content, self.pattern_id, self.temp_section_id, self.diagram_id,
                                            self.category_id)
        return cadena
