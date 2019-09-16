# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


ideal_solutions_patterns_association = Table(
    'ideal_solutions_patterns', Base.metadata,
    Column('ideal_solution_id', Integer, ForeignKey('ideal_solutions.id')),
    Column('pattern_id', Integer, ForeignKey('patterns.id'))
)


class IdealSolution(Base):
    __tablename__ = 'ideal_solutions'

    id = Column(Integer, primary_key=True)
    annotations = Column(String)
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))

    #diagram = relationship("Diagram", backref=backref("ideal_solutions", cascade="all, delete-orphan",
                                                      #single_parent=True))
    diagram = relationship("Diagram", backref="ideal_solution", cascade="all, delete-orphan", single_parent=True, uselist=False)

    # Relation many to many
    patterns = relationship("Pattern", secondary=ideal_solutions_patterns_association, backref='ideal_solutions')

    def __init__(self, annotations, diagram):
        self.annotations = annotations
        self.diagram = diagram

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.annotations, self.diagram_id)
        return cadena
