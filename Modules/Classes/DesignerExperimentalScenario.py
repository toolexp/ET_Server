# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base


class DesignerExperimentalScenario(Base):
    __tablename__ = 'designer_experimental_scenarios'

    id = Column(Integer, primary_key=True)
    designer_type = Column(Integer)   # Indicates whether the designer belongs to the control group or experimental group
    designer_id = Column(Integer, ForeignKey('designers.id'))
    experimental_scenario_id = Column(Integer, ForeignKey('experimental_scenarios.id'))

    designer = relationship("Designer",
                            backref=backref("experimental_scenario_associations", cascade="all, delete-orphan"))
    experimental_scenario = relationship("ExperimentalScenario",
                                         backref=backref("designer_associations", cascade="all, delete-orphan"))

    def __init__(self, designer_type, designer, experimental_scenario):
        self.designer_type = designer_type    # if designer_type=1 --> control group, otherwise experimental group
        self.designer = designer
        self.experimental_scenario = experimental_scenario

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.designer_type, self.designer_id, self.experimental_scenario_id)