# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base


templates_sections_association = Table(
    'templates_sections', Base.metadata,
    Column('template_id', Integer, ForeignKey('templates.id')),
    Column('section_id', Integer, ForeignKey('sections.id'))
)


class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    sections = relationship("Section", secondary=templates_sections_association, backref='templates')


    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.name, self.description)
        return cadena
