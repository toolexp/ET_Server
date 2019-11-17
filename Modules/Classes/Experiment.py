# coding=utf-8

from sqlalchemy import Column, String, Integer
from Modules.Config.base import Base
from Modules.Config.Data import Message


class Experiment(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return '{}¥{}¥{}'.format(self.id, self.name, self.description)

    @staticmethod
    def create(parameters, session):
        # Received --> [name, description]
        experiment_aux = Experiment(parameters[0], parameters[1])
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
        # Received --> [id_experiment, name, description]
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        experiment_aux.name = parameters[1]
        experiment_aux.description = parameters[2]
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
        # Received --> [id_experiment, 'validate']
        if len(parameters) == 2:
            experimetal_sc = session.query(ExperimentalScenario).filter(
                ExperimentalScenario.experiment_id == parameters[0]).first()
            if experimetal_sc:
                return Message(action=5, information=['The experiment is associated to one or more experimental scenarios'],
                               comment='Error selecting register')
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        msg_rspt.information.append(experiment_aux.name)
        msg_rspt.information.append(experiment_aux.description)
        msg_rspt.information.append([])
        for item in experiment_aux.experimental_scenarios:
            msg_rspt.information[2].append(item.__str__())
        session.close()
        return msg_rspt