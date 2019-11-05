# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


sent_solutions_patterns_association = Table(
    'sent_solutions_patterns', Base.metadata,
    Column('sent_solution_id', Integer, ForeignKey('sent_solutions.id')),
    Column('pattern_id', Integer, ForeignKey('patterns.id'))
)


class SentSolution(Base):
    __tablename__ = 'sent_solutions'

    id = Column(Integer, primary_key=True)
    annotations = Column(String)
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    designer_id = Column(Integer, ForeignKey('designers.id'))
    scenario_component_id = Column(Integer, ForeignKey('scenario_components.id'))

    diagram = relationship("Diagram", backref="sent_solutions", cascade="all, delete-orphan", single_parent=True,
                           uselist=False)
    designer = relationship("Designer", backref=backref("sent_solutions", cascade="all, delete-orphan",
                                                        single_parent=True))
    scenario_component = relationship("ScenarioComponent", backref=backref("sent_solutions",
                                                                           cascade="all, delete-orphan",
                                                                           single_parent=True))
    #diagram = relationship("Diagram", backref=backref("sent_solutions", cascade="all, delete-orphan",
                                                      #single_parent=True))
    # Relation many to many
    patterns = relationship("Pattern", secondary=sent_solutions_patterns_association, backref='sent_solutions')

    def __init__(self, annotations, diagram, designer, scenario_component):
        self.annotations = annotations
        self.diagram = diagram
        self.designer = designer
        self.scenario_component = scenario_component

    def __str__(self):
        cadena = '{}¥{}'.format(self.id, self.annotations)
        return cadena
