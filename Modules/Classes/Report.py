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
            from Modules.Classes.Problem import Problem
            # Received --> [id_problem, 'problem']
            current_df = pd.DataFrame(columns=('designer', 'm1', 'm2', 'm3', 'm4'))
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
                current_df = current_df.append({'designer': designer_aux.email, 'm1': measurements_aux[0],
                                                'm2': measurements_aux[1], 'm3': measurements_aux[2],
                                                'm4': measurements_aux[3]}, ignore_index=True)
            msg_rspt.information.append(current_df)
        session.close()
        return msg_rspt
