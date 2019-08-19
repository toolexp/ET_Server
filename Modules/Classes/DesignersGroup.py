# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base

designers_groups_designers_association = Table(
    'designers_groups_designers', Base.metadata,
    Column('designers_group_id', Integer, ForeignKey('designers_groups.id')),
    Column('designer_id', Integer, ForeignKey('designers.id'))
)


class DesignersGroup(Base):
    __tablename__ = 'designers_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    designers = relationship("Designer", secondary=designers_groups_designers_association, backref='designers_groups')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        cadena = '{}:{}:{}:{}'.format(self.id, self.name, self.description, len(self.designers))
        return cadena
