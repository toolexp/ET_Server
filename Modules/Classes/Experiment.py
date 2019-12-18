# coding=utf-8

from sqlalchemy import Column, String, Integer, DateTime
from Modules.Config.base import Base
from Modules.Config.Data import Message
from datetime import datetime


class Experiment(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    design_type = Column(Integer)   # 1-> 'control design', 2-> 'experimental design' (control and experimental group)
    state = Column(String)  # created, executed, finished
    creation_date = Column(DateTime)
    execution_date = Column(DateTime)
    finished_date = Column(DateTime)

    def __init__(self, name, description, design_type):
        self.name = name
        self.description = description
        self.design_type = design_type
        self.state = 'created'
        self.creation_date = datetime.now()
        self.execution_date = None
        self.finished_date = None

    def __str__(self):
        if self.design_type == 1:
            aux = 'One group'
        else:
            aux = 'Two groups'
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, aux, self.state)

    @staticmethod
    def create(parameters, session):
        # Received --> [name, description, design_type]
        experiment_aux = Experiment(parameters[0], parameters[1], parameters[2])
        session.add(experiment_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        # Received --> []
        experiments = session.query(Experiment).all()
        msg_rspt = Message(action=2, information=[])
        for item in experiments:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        if len(parameters) == 3:
            # Received --> [id_experiment, name, description, design_type]
            experiment_aux.name = parameters[1]
            experiment_aux.description = parameters[2]
            experiment_aux.design_type = parameters[3]
        else:
            from Modules.Classes.ExperimentalScenario import ExperimentalScenario
            # Received --> [id_experiment, state]
            if parameters[1] == 'executed' and experiment_aux.state == 'created':   # When an experiment goes from created to executed
                experimental_sc_aux = session.query(ExperimentalScenario).\
                    filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                if not experimental_sc_aux:
                    return Message(action=5, information=['No experimental scenarios created for this experiment. '
                                                          'Create al least one to execute the experiment'],
                                   comment='Error updating register')
                # Change experiment state
                experiment_aux.state = 'executed'
                experiment_aux.execution_date = datetime.now()
                # Change experimental scenarios state, associated with current experiment
                for item in experimental_sc_aux:
                    item.state = 'executed'
            elif parameters[1] == 'finished' and experiment_aux.state == 'executed':    # When an experiment goes from executed to finished

                experimental_sc_aux = session.query(ExperimentalScenario). \
                    filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                # Change experiment state
                experiment_aux.state = 'finished'
                experiment_aux.finished_date = datetime.now()
                # Change experimental scenarios state, associated with current experiment
                for item in experimental_sc_aux:
                    item.state = 'finished'
            else:
                return Message(action=5, information=['The experiment is not in execution. To finish an experiment, it'
                                                      'must be in execution first'],
                               comment='Error updating register')
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        # Received --> [id_experiment]
        from Modules.Classes.ExperimentalScenario import ExperimentalScenario
        experimetal_sc = session.query(ExperimentalScenario).filter(ExperimentalScenario.experiment_id == parameters[0]).first()
        if experimetal_sc:
            return Message(action=5, information=['The experiment is associated to one or more experimental scenarios'],
                           comment='Error deleting register')
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        session.delete(experiment_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        from Modules.Classes.ExperimentalScenario import ExperimentalScenario
        msg_rspt = Message(action=2, information=[])
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        # Received --> [id_experiment, 'validate']
        if len(parameters) == 2:
            if experiment_aux.state == 'finished' or experiment_aux.state == 'executed':
                return Message(action=5, comment='The state of the experiment doesn\'t allow you to change it\'s '
                                                 'information')
            experimetal_sc = session.query(ExperimentalScenario).filter(
                ExperimentalScenario.experiment_id == parameters[0]).first()
            if experimetal_sc:
                msg_rspt.comment = 'The experiment has experimental scenarios associated to it. If you change its\' ' \
                                   'design type, CONFIGURED INFORMATION MAY BE DELETED'
                msg_rspt.action = 6
        msg_rspt.information.append(experiment_aux.name)
        msg_rspt.information.append(experiment_aux.description)
        msg_rspt.information.append(experiment_aux.design_type)
        msg_rspt.information.append(experiment_aux.state)
        msg_rspt.information.append([])
        for item in experiment_aux.experimental_scenarios:
            msg_rspt.information[4].append(item.__str__())
        session.close()
        return msg_rspt