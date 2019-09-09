# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class ScenarioComponent(Base):
    __tablename__ = 'scenario_components'

    id = Column(Integer, primary_key=True)
    experimental_scenario_id = Column(Integer, ForeignKey('experimental_scenarios.id'))
    problem_id = Column(Integer, ForeignKey('problems.id'))

    experimental_scenario = relationship("ExperimentalScenario", backref=backref("scenario_components",
                                                                                 cascade="all, delete-orphan",
                                                                                 single_parent=True))
    problem = relationship("Problem", backref=backref("scenario_components", cascade="all, delete-orphan",
                                                      single_parent=True))
    patterns = relationship("Pattern", secondary="scenario_components_patterns", backref="templates")

    def __init__(self, experimental_scenario, problem):
        self.experimental_scenario = experimental_scenario
        self.problem = problem

    def __str__(self):
        cadena = '{}¥{}¥{}'.format(self.id, self.experimental_scenario_id, self.problem_id)
        return cadena
