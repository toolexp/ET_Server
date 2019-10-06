# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base

class ScenarioComponentPattern(Base):
    __tablename__ = 'scenario_components_patterns'

    id = Column(Integer, primary_key=True)
    pattern_type = Column(Integer)   # Indicates wheter the pattern association is for the control group or experimental group
    scenario_component_id = Column(Integer, ForeignKey('scenario_components.id'))
    pattern_id = Column(Integer, ForeignKey('patterns.id'))
    #UniqueConstraint('scenario_component_id', 'pattern_id', name='UC_scenario_component_id_pattern_id')

    scenario_component = relationship("ScenarioComponent",
                                      backref=backref("pattern_associations", cascade="all, delete-orphan"))
    pattern = relationship("Pattern", backref=backref("scenario_component_associations", cascade="all, delete-orphan"))

    def __init__(self, pattern_type, scenario_component, pattern):
        self.pattern_type = pattern_type    # if pattern_type=1 --> control group, otherwise experimental group
        self.scenario_component = scenario_component
        self.pattern = pattern

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}'.format(self.id, self.pattern_type, self.scenario_component_id, self.pattern_id)
        return cadena

'''class ScenarioComponentPattern(Base):
    __tablename__ = 'scenario_components_patterns'
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

    id = Column(Integer, primary_key=True)
    pattern_type = Column(Integer)   # Indicates wheter the pattern association is for the control group or experimental group
    scenario_component_id = Column(Integer, ForeignKey('scenario_components.id'))
    pattern_id = Column(Integer, ForeignKey('patterns.id'))

    scenario_component = relationship("ScenarioComponent",
                                      backref=backref("pattern_associations", cascade="all, delete-orphan",
                                                      single_parent=True))
    pattern = relationship("Pattern", backref=backref("scenario_component_associations", cascade="all, delete-orphan",
                                                      single_parent=True))

    def __init__(self, pattern_type, scenario_component, pattern):
        self.pattern_type = pattern_type    # if pattern_type=1 --> control group, otherwise experimental group
        self.scenario_component = scenario_component
        self.pattern = pattern

    def __str__(self):
        cadena = '{}¥{}¥{}¥{}'.format(self.id, self.pattern_type, self.scenario_component_id, self.pattern_id)
        return cadena'''
