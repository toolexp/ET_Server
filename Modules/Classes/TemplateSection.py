# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class TemplateSection(Base):
    __tablename__ = 'templates_sections'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, primary_key=True)
    mandatory = Column(Boolean)
    position = Column(Integer)
    template_id = Column(Integer, ForeignKey('templates.id'))
    section_id = Column(Integer, ForeignKey('sections.id'))

    template = relationship("Template", backref=backref("section_associations", cascade="all, delete-orphan", single_parent=True))
    section = relationship("Section", backref=backref("template_associations", cascade="all, delete-orphan", single_parent=True))

    def __init__(self, mandatory, position, template, section):
        self.mandatory = mandatory
        self.position = position
        self.template = template
        self.section = section

    def __str__(self):
        if self.mandatory:
            aux = '✓'
        else:
            aux = ''
        cadena = '{}¥{}¥{}¥{}¥{}¥{}¥{}¥{}¥{}'.format(self.id, self.template_id, self.section_id, self.section.name, self.section.description,
                                   self.section.data_type, self.position, aux, self.section.classification_id)
        return cadena
