# coding=utf-8

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class ExperimentalScenario(Base):
    __tablename__ = 'experimental_scenarios'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    access_code = Column(String)
    start_time = Column(Date)
    end_time = Column(Date)
    scenario_availability = Column(Boolean)
    scenario_lock = Column(Boolean)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    control_group_id = Column(Integer, ForeignKey('designers_groups.id'))
    experimental_group_id = Column(Integer, ForeignKey('designers_groups.id'))

    experiment = relationship("Experiment", backref=backref("experimental_scenarios", cascade="all, delete-orphan",
                                                            single_parent=True))
    control_group = relationship("DesignersGroup", foreign_keys="ExperimentalScenario.control_group_id",
                                 backref=backref("cg_experimental_scenarios", cascade="all, delete-orphan",
                                                 single_parent=True))
    experimental_group = relationship("DesignersGroup", foreign_keys="ExperimentalScenario.experimental_group_id",
                                      backref=backref("eg_experimental_scenarios", cascade="all, delete-orphan",
                                                      single_parent=True))

    def __init__(self, name, description, access_code, start_time, end_time, scenario_availability, scenario_lock,
                 experiment, control_group, experimental_group):
        self.name = name
        self.description = description
        self.access_code = access_code
        self.start_time = start_time
        self.end_time = end_time
        self.scenario_availability = scenario_availability
        self.scenario_lock = scenario_lock
        self.experiment = experiment
        self.control_group = control_group
        self.experimental_group = experimental_group

    def __str__(self):
        cadena = '{}¥{}'.format(self.name, self.description)
        return cadena
