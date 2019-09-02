# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base


class ScenarioComponentPattern(Base):
    __tablename__ = 'scenario_components_patterns'

    id = Column(Integer, primary_key=True)
    scenario_component_id = Column(Integer, ForeignKey('scenario_components.id'))
    pattern_id = Column(Integer, ForeignKey('patterns.id'))
    scenario_component = relationship("ScenarioComponent", back_populates="patterns")
    pattern = relationship("Pattern", back_populates="scenario_components")
    pattern_type = Column(String)

    def __init__(self, pattern_type, scenario_component, pattern):
        self.pattern_type = pattern_type
        self.scenario_component = scenario_component
        self.pattern = pattern

    def __str__(self):
        cadena = '{}'.format(self.pattern_type)
        return cadena
