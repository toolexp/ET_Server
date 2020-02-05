# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, and_, String
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message, get_experiment_report
from Modules.Classes.Experiment import Experiment


class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_path = Column(String)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))

    experiment = relationship("Experiment", backref="report", cascade="all, delete-orphan", single_parent=True,
                              uselist=False)

    def __init__(self, name, file_path, experiment):
        self.name = name
        self.file_path = file_path
        self.experiment = experiment

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.name, self.file_path, self.experiment_id)

    @staticmethod
    def create(parameters, session):
        # Generating a report
        # Received --> [id_experiment]
        # Returned --> [file_name, zipped_experiment_folder_bytes]
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
        msg_rspt = Message(action=2, information=[file_name, file_bytes], comment='Register created successfully')
        return msg_rspt

    def read(parameters, session):
        msg_rspt = Message(action=2, information=[])
        import pandas as pd
        if parameters[1] == 'problem':
            from Modules.Classes.Designer import Designer
            from Modules.Classes.Measurement import Measurement
            from Modules.Classes.Metric import Metric
            from Modules.Classes.Problem import Problem
            # Received --> [id_problem, 'problem']
            current_query = session.query(Measurement). \
                with_entities(Designer.email.label('designer'), Metric.name.label('metric_type'),
                              Measurement.value.label('measurement')). \
                join(Problem.measurements).join(Measurement.designer).join(Measurement.metric). \
                filter(Problem.id == parameters[0]).statement
            current_df = pd.read_sql_query(current_query, session.bind)
            msg_rspt.information.append(current_df)
        session.close()
        return msg_rspt
