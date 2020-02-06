# coding=utf-8
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Metric import Metric
from Modules.Classes.Problem import Problem


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    acquisition_start_date = Column(DateTime)
    acquisition_end_date = Column(DateTime)
    metric_id = Column(Integer, ForeignKey('metrics.id'))
    designer_id = Column(Integer, ForeignKey('designers.id'))
    problem_id = Column(Integer, ForeignKey('problems.id'))

    metric = relationship("Metric", backref=backref("measurements", cascade="all, delete-orphan",
                                                    single_parent=True))
    designer = relationship("Designer", backref=backref("measurements", cascade="all, delete-orphan",
                                                        single_parent=True))
    problem = relationship("Problem", backref=backref("measurements", cascade="all, delete-orphan", single_parent=True))

    def __init__(self, value, acquisition_start_date, acquisition_end_date, metric, designer, problem):
        self.value = value
        self.acquisition_start_date = acquisition_start_date
        self.acquisition_end_date = acquisition_end_date
        self.metric = metric
        self.designer = designer
        self.problem = problem

    def __str__(self):
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.metric_id, self.problem_id, self.designer_id, self.value)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.Designer import Designer
        # Received --> [value, acquisition_start_date, acquisition_end_date, metric_id, designer_id, problem_id]
        # First check if the measurements for the problem do not exist (it may exist if experimenter finished an
        # experiment while it was in execution and any designer was active)
        existing_measurement = session.query(Measurement).filter(and_(Measurement.problem_id == parameters[5],
                                                                      Measurement.designer_id == parameters[4],
                                                                      Measurement.metric_id == parameters[3])).all()
        if not existing_measurement:
            metric_aux = session.query(Metric).filter(Metric.id == parameters[3]).first()
            designer_aux = session.query(Designer).filter(Designer.id == parameters[4]).first()
            problem_aux = session.query(Problem).filter(Problem.id == parameters[5]).first()
            measurement_aux = Measurement(parameters[0], parameters[1], parameters[2], metric_aux, designer_aux,
                                          problem_aux)
            session.add(measurement_aux)
            session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt
