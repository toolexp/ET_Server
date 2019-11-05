# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    metric_id = Column(Integer, ForeignKey('metrics.id'))
    designer_id = Column(Integer, ForeignKey('designers.id'))
    scenario_component_id = Column(Integer, ForeignKey('scenario_components.id'))

    metric = relationship("Metric", backref=backref("measurements", cascade="all, delete-orphan",
                                                      single_parent=True))
    designer = relationship("Designer", backref=backref("measurements", cascade="all, delete-orphan",
                                                        single_parent=True))
    scenario_component = relationship("ScenarioComponent", backref=backref("measurements",
                                                                           cascade="all, delete-orphan",
                                                                           single_parent=True))

    def __init__(self, value, metric, designer, scenario_component):
        self.value = value
        self.metric = metric
        self.designer = designer
        self.scenario_component = scenario_component

    def __str__(self):
        cadena = '{}¥{}'.format(self.id, self.value)
        return cadena
