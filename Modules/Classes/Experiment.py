from sqlalchemy import Column, String, Integer, DateTime, and_
from Modules.Config.base import Base
from Modules.Config.Data import Message
from datetime import datetime


class Experiment(Base):
    """
    A class used to represent an experiment. An experiment object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param name: name of the experiment
    :type name: str
    :param description: description of the experiment
    :type description: str
    :param design_type: indicates the type of design of the experiment (one or two groups of designers)
    :type design_type: int
    :param state: current state of the experiment. It may be: created, execution or finished
    :type state: str
    :param creation_date: datetime when the experiment was created
    :type creation_date: datetime
    :param execution_date: datetime when the experiment was executed (made it available for designers)
    :type execution_date: datetime
    :param finished_date: datetime when the experiment was finished (manually or automatically)
    :type finished_date: datetime
    """

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
        """
        Constructor of the class
        """
        self.name = name
        self.description = description
        self.design_type = design_type
        self.state = 'created'
        self.creation_date = datetime.now()
        self.execution_date = None
        self.finished_date = None

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.design_type, self.state)

    @staticmethod
    def create(parameters, session):
        """
        Creates an 'Experiment' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
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
        """
        Retrieves a list of 'Experiments' registered into the DB. The list contains a string representation of
        each 'Experiment' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        msg_rspt = Message(action=2, information=[])
        # Received --> ['finished']
        if len(parameters) == 1:    # Asking for finished experiments (to get reports)
            experiments = session.query(Experiment).filter(Experiment.state == 'finished').all()
        # Received --> []
        else:   # Asking for all experiments
            experiments = session.query(Experiment).all()
        for item in experiments:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        """
        Updates an 'Experiment' object from the DB, the id and new data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        if len(parameters) == 4:    # Update information of the experiment
            # Received --> [id_experiment, name, description, design_type]
            experiment_aux.name = parameters[1]
            experiment_aux.description = parameters[2]
            experiment_aux.design_type = parameters[3]
        else:   # Update state of the experiment
            # Received --> [id_experiment, state]
            from Modules.Classes.ExperimentalScenario import ExperimentalScenario
            if parameters[1] == 'execution':   # When an experiment is executed
                if experiment_aux.state == 'created':
                    experimental_sc_aux = session.query(ExperimentalScenario).\
                        filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                    if not experimental_sc_aux:     # Any scenario configured yet
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
                elif experiment_aux.state == 'execution':    # When need to execute new scenarios after having executed
                    # the experiment, if new scenarios were created
                    experimental_sc_aux = session.query(ExperimentalScenario). \
                        filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                    executed_scenarios = True
                    for item in experimental_sc_aux:
                        if item.state == 'created':
                            item.state = 'execution'
                            item.execution_date = datetime.now()
                            executed_scenarios = False
                    if executed_scenarios:  # If no new scenarios were created
                        return Message(action=5, information=['All scenarios configured are already in execution'],
                                       comment='Error updating register')
                else:   # Experimental scenario is finished, can not execute
                    return Message(action=5, information=['The experiment is finished, can not execute'],
                                   comment='Error updating register')
            elif parameters[1] == 'finished':    # When an experiment finishes
                if experiment_aux.state == 'execution':     # When current state of experiment is 'execution'
                    experimental_sc_aux = session.query(ExperimentalScenario). \
                        filter(ExperimentalScenario.experiment_id == parameters[0]).all()
                    # Change experimental scenarios state, associated with current experiment
                    for item in experimental_sc_aux:
                        if item.state == 'created':  # At least one scenario has not been executed yet
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
                    # Section to create empty measurements (-1) for all designers that have not executed the scenarios
                    metrics = session.query(Metric).all()
                    current_date = datetime.now()
                    for item in experimental_sc_aux:
                        all_designers = session.query(Designer). \
                            join(Designer.experimental_scenario_associations). \
                            join(DesignerExperimentalScenario.experimental_scenario).\
                            filter(ExperimentalScenario.id == item.id).all()
                        problems = session.query(Problem). \
                            join(Problem.experimental_scenario). \
                            filter(ExperimentalScenario.id == item.id).all()
                        # Here creates the empty measurements for scenarios that were not executed by designers
                        for designer_aux in all_designers:
                            for problem_aux in problems:
                                existing_measurement = session.query(Measurement).\
                                    filter(and_(Measurement.designer_id == designer_aux.id,
                                                Measurement.problem_id == problem_aux.id)).all()
                                if not existing_measurement:    # If at least one designer has a remaining measurement,
                                    # it has to be created (-1)
                                    for metric_aux in metrics:
                                        measurement_aux = Measurement(float(-1), current_date, current_date, metric_aux,
                                                                      designer_aux, problem_aux)
                                        session.add(measurement_aux)
                    # Change experiment state
                    experiment_aux.state = 'finished'
                    experiment_aux.finished_date = datetime.now()
                elif experiment_aux.state == 'finished':    # Current state is finished
                    return Message(action=5, information=['The experiment is already finished'],
                                   comment='Error updating register')
                else:   # Current state is created, can not finish yet
                    return Message(action=5, information=['The experiment is created, first execute to finish it'],
                                   comment='Error updating register')
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes an 'Experiment' object from the DB. The 'parameters' contains de id of the 'Experiment' object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
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
        """
        Retrieve information (attributes) of an 'Experiment' object from the DB. The 'parameters' contains de id of
        the desired 'Experimenter'.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.ExperimentalScenario import ExperimentalScenario
        msg_rspt = Message(action=2, information=[])
        experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
        if len(parameters) == 2:    # When an experiment is selected for updating its information
            if experiment_aux.state == 'finished' or experiment_aux.state == 'execution':
                return Message(action=5, comment='The state of the experiment doesn\'t allow you to change it\'s '
                                                 'information')
            experimetal_sc = session.query(ExperimentalScenario).filter(
                ExperimentalScenario.experiment_id == parameters[0]).first()
            if experimetal_sc:  # The experiment has at least one configured scenario, WARNING when updating design type
                msg_rspt.comment = 'The experiment has experimental scenarios associated to it. If you change its\' ' \
                                   'design type, CONFIGURED INFORMATION MAY BE DELETED'
                msg_rspt.action = 6
        # Select attributes of the experiment
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