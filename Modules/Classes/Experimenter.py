# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base

experimenters_experiments_association = Table(
    'experimenters_experiments', Base.metadata,
    Column('experimenter_id', Integer, ForeignKey('experimenters.id')),
    Column('experiment_id', Integer, ForeignKey('experiments.id'))
)


class Experimenter(Base):
    __tablename__ = 'experimenters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)

    experiments = relationship("Experiment", secondary=experimenters_experiments_association, backref='experimenters')

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.name, self.surname)
        return cadena