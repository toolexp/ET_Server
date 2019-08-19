# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    ideal_solution_id = Column(Integer, ForeignKey('ideal_solutions.id'))
    ideal_solution = relationship("IdealSolution", backref=backref("problems", cascade="all, delete-orphan",
                                                                   single_parent=True))

    def __init__(self, name, description, ideal_solution):
        self.name = name
        self.description = description
        self.ideal_solution = ideal_solution

    def __str__(self):
        cadena = '{}:{}:{}'.format(self.id, self.name, self.description)
        return cadena
