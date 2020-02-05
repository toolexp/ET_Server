# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float
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
        metric_aux = session.query(Metric).filter(Metric.id == parameters[3]).first()
        designer_aux = session.query(Designer).filter(Designer.id == parameters[4]).first()
        problem_aux = session.query(Problem).filter(Problem.id == parameters[5]).first()
        measurement_aux = Measurement(parameters[0], parameters[1], parameters[2], metric_aux, designer_aux, problem_aux)
        session.add(measurement_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        # Received --> []
        measurements = session.query(Measurement).all()
        msg_rspt = Message(action=2, information=[])
        for item in measurements:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        from Modules.Classes.Designer import Designer
        # Received --> [id_measurement, value, date_acquisition, metric_id, designer_id, scenario_comp_id]
        measurement_aux = session.query(Measurement).filter(Measurement.id == parameters[0]).first()
        metric_aux = session.query(Metric).filter(Metric.id == parameters[3]).first()
        designer_aux = session.query(Designer).filter(Designer.id == parameters[4]).first()
        problem_aux = session.query(Problem).filter(Problem.id == parameters[5]).first()
        measurement_aux.value = parameters[1]
        measurement_aux.date_acquisition = parameters[2]
        measurement_aux.metric = metric_aux
        measurement_aux.designer = designer_aux
        measurement_aux.scenario_component = problem_aux
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        # Received --> [id_measurement]
        measurement_aux = session.query(Measurement).filter(Measurement.id == parameters[0]).first()
        session.delete(measurement_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        measurement_aux = session.query(Measurement).filter(Measurement.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(measurement_aux.value)
        msg_rspt.information.append(measurement_aux.acquisition_start_date)
        msg_rspt.information.append(measurement_aux.acquisition_end_date)
        msg_rspt.information.append(measurement_aux.metric_id)
        msg_rspt.information.append(measurement_aux.designer_id)
        msg_rspt.information.append(measurement_aux.problem_id)
        session.close()
        return msg_rspt
