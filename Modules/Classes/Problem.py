# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    ideal_solution_id = Column(Integer, ForeignKey('ideal_solutions.id'))

    #ideal_solution = relationship("IdealSolution", backref=backref("problems", cascade="all, delete-orphan",
                                                                   #single_parent=True))

    #ideal_solution = relationship("IdealSolution", foreign_keys=ideal_solution_id, post_update=True, cascade="all, delete-orphan",
                                  #single_parent=True)
    ideal_solution = relationship("IdealSolution", backref="problem", cascade="all, delete-orphan", single_parent=True,
                                  uselist=False)

    def __init__(self, name, description, ideal_solution):
        self.name = name
        self.description = description
        self.ideal_solution = ideal_solution

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.ideal_solution_id)
        return cadena
