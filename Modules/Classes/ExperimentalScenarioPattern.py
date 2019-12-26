# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message

from Modules.Classes.Pattern import Pattern


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
        self.pattern_type = pattern_type    # if pattern_type=1 --> experimental group, otherwise control group
        self.experimental_scenario = experimental_scenario
        self.pattern = pattern

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.pattern_type, self.experimental_scenario_id, self.pattern_id)

    @staticmethod
    def read(parameters, session):
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 0:
            exp_scenarios_pat = session.query(ExperimentalScenarioPattern).all()
            for item in exp_scenarios_pat:
                msg_rspt.information.append(item.__str__())
        else:  # return patterns separated in experimental and control group
            # Received --> [id_exp_scenario]
            exp_scenarios_pat = session.query(ExperimentalScenarioPattern).filter(
                ExperimentalScenarioPattern.experimental_scenario_id == parameters[0]).all()
            exp_patterns = []
            ctrl_patterns = []
            for item in exp_scenarios_pat:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item.pattern_id).first()
                if item.pattern_type == 1:  # if pattern_type=1 --> experimental group, otherwise control group
                    exp_patterns.append(pattern_aux.__str__())
                else:
                    ctrl_patterns.append(pattern_aux.__str__())
            msg_rspt.information.append(exp_patterns)
            msg_rspt.information.append(ctrl_patterns)
        session.close()
        return msg_rspt