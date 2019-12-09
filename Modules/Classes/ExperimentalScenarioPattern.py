# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class ExperimentalScenarioPattern(Base):
    __tablename__ = 'experimental_scenarios_patterns'

    id = Column(Integer, primary_key=True)
    pattern_type = Column(Integer)   # Indicates wheter the pattern association is for the control group or experimental group
    experimental_scenario_id = Column(Integer, ForeignKey('experimental_scenarios.id'))
    pattern_id = Column(Integer, ForeignKey('patterns.id'))

    experimental_scenario = relationship("ExperimentalScenario",
                                         backref=backref("pattern_associations", cascade="all, delete-orphan"))
    pattern = relationship("Pattern", backref=backref("experimental_scenario_associations", cascade="all, delete-orphan"))

    def __init__(self, pattern_type, experimental_scenario, pattern):
        self.pattern_type = pattern_type    # if pattern_type=1 --> control group, otherwise experimental group
        self.experimental_scenario = experimental_scenario
        self.pattern = pattern

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.pattern_type, self.experimental_scenario_id, self.pattern_id)
