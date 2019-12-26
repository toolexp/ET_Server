# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message


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
        self.designer_type = designer_type    # if designer_type=1 --> experimental group, otherwise control group
        self.designer = designer
        self.experimental_scenario = experimental_scenario

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.designer_type, self.designer_id, self.experimental_scenario_id)

    @staticmethod
    def read(parameters, session):
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 0:
            des_exp_scenarios = session.query(DesignerExperimentalScenario).all()
            for item in des_exp_scenarios:
                msg_rspt.information.append(item.__str__())
        else:   #return designers separated in experimental and control group
            # Received --> [id_exp_scenario]
            from Modules.Classes.Designer import Designer
            des_exp_scenarios = session.query(DesignerExperimentalScenario).filter(
                DesignerExperimentalScenario.experimental_scenario_id == parameters[0]).all()
            exp_designers = []
            ctrl_designers = []
            for item in des_exp_scenarios:
                designer_aux = session.query(Designer).filter(Designer.id == item.designer_id).first()
                if item.designer_type == 1:   # if designer_type=1 --> experimental group, otherwise control group
                    exp_designers.append(designer_aux.__str__())
                else:
                    ctrl_designers.append(designer_aux.__str__())
            msg_rspt.information.append(exp_designers)
            msg_rspt.information.append(ctrl_designers)
        session.close()
        return msg_rspt