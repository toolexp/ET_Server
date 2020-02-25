from sqlalchemy import Column, Integer, ForeignKey, and_, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message, get_experiment_report
from Modules.Classes.Experiment import Experiment


class Report(Base):
    """
    A class used to represent an experiment report. A report object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param name: report name (filename)
    :type name: str
    :param file_path: full path of the file (report) stored in the server
    :type file_path: str
    :param experiment_id: identifier of the experiment object that the report is associated with. This is a foreign key
    :type experiment_id: int
    :param experiment: experiment object that the report is associated with
    :type experiment: Modules.Classes.Experiment.Experiment
    """
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_path = Column(String)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))

    experiment = relationship("Experiment", backref="report", cascade="all, delete-orphan", single_parent=True,
                              uselist=False)

    def __init__(self, name, file_path, experiment):
        """
        Constructor of the class
        """
        self.name = name
        self.file_path = file_path
        self.experiment = experiment

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}¥{}'.format(self.id, self.name, self.file_path, self.experiment_id)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'Report' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable. Creates a report file if it does not exist in the server

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_experiment]
        report_aux = session.query(Report).filter(Report.experiment_id == parameters[0]).first()
        if not report_aux:
            experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
            file_name, file_path = get_experiment_report(experiment_aux, session)
            report_aux = Report(file_name, file_path, experiment_aux)
            session.add(report_aux)
            session.commit()
        else:
            file_name = report_aux.name
            file_path = report_aux.file_path
        session.close()
        myfile = open(file_path, 'rb')
        file_bytes = myfile.read()
        myfile.close()
        # Returned --> [file_name, zipped_experiment_folder_bytes]
        msg_rspt = Message(action=2, information=[file_name, file_bytes], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a dataframe with measurements of the 'Report' detailed as they are requested: full experiment, an
        experimental scenario or an specific problem

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        msg_rspt = Message(action=2, information=[])
        import pandas as pd
        current_df = pd.DataFrame(columns=('id', 'variable', 'm1', 'm2', 'm3', 'm4'))
        if parameters[1] == 'problem':  # Asks for measurements of an specific problem
            from Modules.Classes.Designer import Designer
            from Modules.Classes.Measurement import Measurement
            from Modules.Classes.Problem import Problem
            # Received --> [id_problem, 'problem']
            designers = session.query(Designer). \
                join(Designer.measurements).join(Measurement.problem). \
                filter(Problem.id == parameters[0]).all()
            for designer_aux in designers:
                measurements = session.query(Measurement). \
                    join(Designer.measurements).join(Measurement.problem). \
                    filter(and_(Problem.id == parameters[0], Designer.id == designer_aux.id)).all()
                measurements_aux = [None, None, None, None]
                for item in measurements:
                    if item.metric_id == 1:
                        measurements_aux[0] = item.value if item.value >= 0 else None
                    elif item.metric_id == 2:
                        measurements_aux[1] = item.value if item.value >= 0 else None
                    elif item.metric_id == 3:
                        measurements_aux[2] = item.value if item.value >= 0 else None
                    else:
                        measurements_aux[3] = item.value if item.value >= 0 else None
                current_df = current_df.append({'id': designer_aux.id, 'variable': designer_aux.email,
                                                'm1': measurements_aux[0], 'm2': measurements_aux[1],
                                                'm3': measurements_aux[2], 'm4': measurements_aux[3]},
                                               ignore_index=True)
        elif parameters[1] == 'scenario':   # Asks for measurements of an specific experimental scenario
            from Modules.Classes.ExperimentalScenario import ExperimentalScenario
            from Modules.Classes.Designer import Designer
            from Modules.Classes.Measurement import Measurement
            from Modules.Classes.Problem import Problem
            # Received --> [id_scenario, 'scenario']
            problems = session.query(Problem).join(Problem.experimental_scenario).\
                filter(ExperimentalScenario.id == parameters[0]).all()
            for problem_aux in problems:
                measurements_aux = []
                for item in range(1, 5):
                    average = session.query(func.avg(Measurement.value).label('average')). join(Measurement.problem).\
                        filter(and_(Problem.id == problem_aux.id, Measurement.metric_id == item,
                                    Measurement.value >= 0)).all()
                    measurements_aux.append(average[0].average)
                current_df = current_df.append({'id': 'X', 'variable': problem_aux.brief_description,
                                                'm1': measurements_aux[0], 'm2': measurements_aux[1],
                                                'm3': measurements_aux[2], 'm4': measurements_aux[3]},
                                               ignore_index=True)
        else:   # Asks for measurements of an specific experiment
            from Modules.Classes.ExperimentalScenario import ExperimentalScenario
            from Modules.Classes.Designer import Designer
            from Modules.Classes.Measurement import Measurement
            from Modules.Classes.Problem import Problem
            # Received --> [id_experiment, 'experiment']
            scenarios = session.query(ExperimentalScenario).join(ExperimentalScenario.experiment). \
                filter(Experiment.id == parameters[0]).all()
            for scenario_aux in scenarios:
                measurements_aux = []
                for item in range(1, 5):
                    average = session.query(func.avg(Measurement.value).label('average')).join(Measurement.problem). \
                        join(Problem.experimental_scenario). \
                        filter(and_(ExperimentalScenario.id == scenario_aux.id, Measurement.metric_id == item,
                                    Measurement.value >= 0)).all()
                    measurements_aux.append(average[0].average)
                current_df = current_df.append({'id': 'X', 'variable': scenario_aux.title,
                                                'm1': measurements_aux[0], 'm2': measurements_aux[1],
                                                'm3': measurements_aux[2], 'm4': measurements_aux[3]},
                                               ignore_index=True)
        msg_rspt.information.append(current_df)
        session.close()
        return msg_rspt
