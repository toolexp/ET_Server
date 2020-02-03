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
    state = Column(String)  # created, execution, finished
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
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.design_type, self.state)

    @staticmethod
    def create(parameters, session):
        # Received --> [name, description, design_type]
        experiment_aux = Experiment(parameters[0], parameters[1], parameters[2])
        session.add(experiment_aux)
        session.commit()
        new_experiment_aux = session.query(Experiment).order_by(Experiment.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[new_experiment_aux.id], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        # Received --> ['finished']
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 1:    # Asking for finished experiments (reports)
            experiments = session.query(Experiment).filter(Experiment.state == 'finished').all()
        else:
            experiments = session.query(Experiment).all()
        for item in experiments:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        if len(parameters) == 4:
            # Received --> [id_experiment, name, description, design_type]
            experiment_aux.name = parameters[1]
            experiment_aux.description = parameters[2]
            experiment_aux.design_type = parameters[3]
        else:
            from Modules.Classes.ExperimentalScenario import ExperimentalScenario
            # Received --> [id_experiment, state]
            if parameters[1] == 'execution':   # When an experiment goes from created to execution
                if experiment_aux.state == 'created':
                    experimental_sc_aux = session.query(ExperimentalScenario).\
                        filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                    if not experimental_sc_aux:
                        return Message(action=5, information=['No experimental scenarios created for this experiment. '
                                                              'Create al least one to execute the experiment'],
                                       comment='Error updating register')
                    # Change experiment state
                    experiment_aux.state = 'execution'
                    experiment_aux.execution_date = datetime.now()
                    # Change experimental scenarios state, associated with current experiment
                    for item in experimental_sc_aux:
                        item.state = 'execution'
                        item.execution_date = datetime.now()
                elif experiment_aux.state == 'execution':    # When need to execute new scenarios after having executed the experiment
                    experimental_sc_aux = session.query(ExperimentalScenario). \
                        filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                    executed_scenarios = True
                    for item in experimental_sc_aux:
                        if item.state == 'created':
                            item.state = 'execution'
                            item.execution_date = datetime.now()
                            executed_scenarios = False
                    if executed_scenarios:
                        return Message(action=5, information=['All scenarios configured are already in execution'],
                                       comment='Error updating register')
                else:   # Experimental scenario is finished
                    return Message(action=5, information=['The experiment is finished, can not execute'],
                                   comment='Error updating register')
            elif parameters[1] == 'finished':    # When an experiment goes from execution to finished
                if experiment_aux.state == 'execution':
                    experimental_sc_aux = session.query(ExperimentalScenario). \
                        filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                    # Change experimental scenarios state, associated with current experiment
                    for item in experimental_sc_aux:
                        if item.state == 'created':  # An scenario has not been executed yet
                            return Message(action=5, information=['At least one associated scenario has not been '
                                                                  'executed yet. Execute all scenarios first to finish '
                                                                  'the experiment'],
                                           comment='Error updating register')
                        item.state = 'finished'
                        item.finished_date = datetime.now()
                    from Modules.Classes.Metric import Metric
                    from Modules.Classes.Measurement import Measurement
                    from Modules.Classes.Designer import Designer
                    from Modules.Classes.Problem import Problem
                    from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
                    # Section to create empty measurement (-1) for all designers that have not executed the scenarios
                    all_designers = session.query(Designer). \
                        join(Designer.experimental_scenario_associations). \
                        join(DesignerExperimentalScenario.experimental_scenario).\
                        join(ExperimentalScenario.experiment).filter(Experiment.id == parameters[0]).all()
                    done_designers = session.query(Designer). \
                        join(Designer.measurements). \
                        join(Measurement.problem).join(Problem.experimental_scenario).\
                        join(ExperimentalScenario.experiment).filter(Experiment.id == parameters[0]).all()
                    for item in done_designers:
                        if item in all_designers:
                            all_designers.remove(item)
                    if all_designers:   # If at least one designer is remaining a measurement, it has to be created (-1)
                        problems = session.query(Problem). \
                            join(Problem.experimental_scenario). \
                            join(ExperimentalScenario.experiment).filter(Experiment.id == parameters[0]).all()
                        metrics = session.query(Metric).all()
                        current_date = datetime.now()
                        # Here creates the empty measurements
                        for designer_aux in all_designers:
                            for problem_aux in problems:
                                for metric_aux in metrics:
                                    measurement_aux = Measurement(-1, current_date, current_date, metric_aux,
                                                                  designer_aux, problem_aux)
                                    session.add(measurement_aux)
                    # Change experiment state
                    experiment_aux.state = 'finished'
                    experiment_aux.finished_date = datetime.now()
                elif experiment_aux.state == 'finished':
                    return Message(action=5, information=['The experiment is already finished'],
                                   comment='Error updating register')
                else:   # Experimental scenario is created
                    return Message(action=5, information=['The experiment is created, first execute to finish it'],
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
        if len(parameters) == 2:
            if experiment_aux.state == 'finished' or experiment_aux.state == 'execution':
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
        msg_rspt.information.append(experiment_aux.creation_date)
        msg_rspt.information.append(experiment_aux.execution_date)
        msg_rspt.information.append(experiment_aux.finished_date)
        for item in experiment_aux.experimental_scenarios:
            msg_rspt.information[4].append(item.__str__())
        session.close()
        return msg_rspt