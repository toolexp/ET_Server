# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Experiment import Experiment
from Modules.Classes.Measurement import Measurement
from Modules.Classes.ScenarioComponent import ScenarioComponent


class ExperimentalScenario(Base):
    __tablename__ = 'experimental_scenarios'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    access_code = Column(String)
    # start_time = Column(Time)
    # end_time = Column(Time)
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

    def __init__(self, name, description, access_code, scenario_availability, scenario_lock,
                 experiment, control_group, experimental_group):
        self.name = name
        self.description = description
        self.access_code = access_code
        self.scenario_availability = scenario_availability
        self.scenario_lock = scenario_lock
        self.experiment = experiment
        self.control_group = control_group
        self.experimental_group = experimental_group

    '''def __init__(self, name, description, access_code, scenario_availability, scenario_lock, start_time, end_time,
                 experiment, control_group, experimental_group):
        self.name = name
        self.description = description
        self.access_code = access_code
        self.scenario_availability = scenario_availability
        self.scenario_lock = scenario_lock
        self.start_time = start_time
        self.end_time = end_time
        self.experiment = experiment
        self.control_group = control_group
        self.experimental_group = experimental_group'''

    def __str__(self):
        if self.scenario_availability:
            aux_av = '✓'
        else:
            aux_av = ''
        if self.scenario_lock:
            aux_lck = '✓'
        else:
            aux_lck = ''
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, aux_av, aux_lck)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.DesignersGroup import DesignersGroup
        # Received --> [name, description, access_code, scenario_availability, scenario_lock, experiment_id, control_group_id, experimental_group_id]
        experiment = session.query(Experiment).filter(Experiment.id == parameters[5]).first()
        control_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[6]).first()
        experimental_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[7]).first()
        exp_sc_aux = ExperimentalScenario(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4],
                                          experiment, control_group, experimental_group)
        session.add(exp_sc_aux)
        session.commit()
        new_exp_sc_aux = session.query(ExperimentalScenario).order_by(ExperimentalScenario.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[new_exp_sc_aux.id], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        from Modules.Classes.Designer import Designer
        from Modules.Classes.DesignersGroup import DesignersGroup
        if len(parameters) == 0:
            exp_scenarios = session.query(ExperimentalScenario).all()
        elif len(parameters) == 1:
            # Received --> [id_experiment]
            exp_scenarios = session.query(ExperimentalScenario).filter(
                ExperimentalScenario.experiment_id == parameters[0]).all()
        else:
            # Received --> ['my scenarios', id_designer] (When a designer retrieves available scenarios for him)
            exp_scenarios_ctrl = session.query(ExperimentalScenario). \
                join(ExperimentalScenario.control_group). \
                join(DesignersGroup.designers).filter(and_(Designer.id == parameters[1],
                                                           ExperimentalScenario.scenario_availability == True)).all()
            exp_scenarios_exp = session.query(ExperimentalScenario). \
                join(ExperimentalScenario.experimental_group). \
                join(DesignersGroup.designers).filter(and_(Designer.id == parameters[1],
                                                           ExperimentalScenario.scenario_availability == True)).all()
            exp_scenarios_ctrl += exp_scenarios_exp
            exp_scenarios_done = session.query(ExperimentalScenario). \
                join(ExperimentalScenario.scenario_components). \
                join(ScenarioComponent.measurements).filter(Measurement.designer_id == parameters[1]).all()
            for item in exp_scenarios_done:
                if item in exp_scenarios_ctrl:
                    exp_scenarios_ctrl.remove(item)
            exp_scenarios = exp_scenarios_ctrl
        msg_rspt = Message(action=2, information=[])
        for item in exp_scenarios:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        from Modules.Classes.DesignersGroup import DesignersGroup
        if len(parameters) == 3:
            # Received --> ['change_availability', id_exp_sc, new_state]
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[1]).first()
            exp_sc_aux.scenario_availability = parameters[2]
        elif len(parameters) == 2:
            # Received --> ['lock_scenario', id_exp_sc]
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[1]).first()
            exp_sc_aux.scenario_lock = True
        else:
            # Received --> [id_exp_sc, name, description, access_code, scenario_availability, scenario_lock, experiment_id, control_group_id, experimental_group_id]
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
            experiment = session.query(Experiment).filter(Experiment.id == parameters[6]).first()
            control_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[7]).first()
            experimental_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[8]).first()
            exp_sc_aux.name = parameters[1]
            exp_sc_aux.description = parameters[2]
            exp_sc_aux.access_code = parameters[3]
            exp_sc_aux.scenario_availability = parameters[4]
            exp_sc_aux.scenario_lock = parameters[5]
            exp_sc_aux.experiment = experiment
            exp_sc_aux.control_group = control_group
            exp_sc_aux.experimental_group = experimental_group
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        # Received --> [id_exp_scenario]
        exp_scenario_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
        session.delete(exp_scenario_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 1:
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
            msg_rspt.information.append(exp_sc_aux.name)
            msg_rspt.information.append(exp_sc_aux.description)
            msg_rspt.information.append(exp_sc_aux.access_code)
            msg_rspt.information.append(exp_sc_aux.scenario_availability)
            msg_rspt.information.append(exp_sc_aux.scenario_lock)
            msg_rspt.information.append(exp_sc_aux.experiment_id)
            msg_rspt.information.append(exp_sc_aux.control_group_id)
            msg_rspt.information.append(exp_sc_aux.experimental_group_id)
            session.close()
            return msg_rspt
        else:
            from Modules.Classes.DesignersGroup import DesignersGroup
            from Modules.Classes.Designer import Designer
            # Received --> [id_designer, id_exp_scenario] # Get role for current experimental scenario
            # (control or experimental)
            exp_scenarios_ctrl = session.query(ExperimentalScenario). \
                join(ExperimentalScenario.control_group). \
                join(DesignersGroup.designers).filter(and_(Designer.id == parameters[0],
                                                           ExperimentalScenario.id == parameters[1])).first()
            if exp_scenarios_ctrl:
                msg_rspt.information.append('control')
                return msg_rspt
            exp_scenarios_exp = session.query(ExperimentalScenario). \
                join(ExperimentalScenario.experimental_group). \
                join(DesignersGroup.designers).filter(and_(Designer.id == parameters[0],
                                                           ExperimentalScenario.id == parameters[1])).first()
            if exp_scenarios_exp:
                msg_rspt.information.append('experimental')
                return msg_rspt
