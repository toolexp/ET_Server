# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Metric import Metric
from Modules.Classes.ScenarioComponent import ScenarioComponent


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    date_acquisition = Column(DateTime)
    metric_id = Column(Integer, ForeignKey('metrics.id'))
    designer_id = Column(Integer, ForeignKey('designers.id'))
    scenario_component_id = Column(Integer, ForeignKey('scenario_components.id'))

    metric = relationship("Metric", backref=backref("measurements", cascade="all, delete-orphan",
                                                    single_parent=True))
    designer = relationship("Designer", backref=backref("measurements", cascade="all, delete-orphan",
                                                        single_parent=True))
    scenario_component = relationship("ScenarioComponent", backref=backref("measurements",
                                                                           cascade="all, delete-orphan",
                                                                           single_parent=True))

    def __init__(self, value, date_acquisition, metric, designer, scenario_component):
        self.value = value
        self.date_acquisition = date_acquisition
        self.metric = metric
        self.designer = designer
        self.scenario_component = scenario_component

    def __str__(self):
        return '{}¥{}'.format(self.id, self.value, self.date_acquisition)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.Designer import Designer
        # Received --> [value, date_acquisition, metric_id, designer_id, scenario_comp_id]
        metric_aux = session.query(Metric).filter(Metric.id == parameters[2]).first()
        designer_aux = session.query(Designer).filter(Designer.id == parameters[3]).first()
        scenario_comp_aux = session.query(ScenarioComponent).filter(ScenarioComponent.id == parameters[4]).first()
        measurement_aux = Measurement(parameters[0], parameters[1], metric_aux, designer_aux, scenario_comp_aux)
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
        scenario_comp_aux = session.query(ScenarioComponent).filter(ScenarioComponent.id == parameters[5]).first()
        measurement_aux.value = parameters[1]
        measurement_aux.date_acquisition = parameters[2]
        measurement_aux.metric = metric_aux
        measurement_aux.designer = designer_aux
        measurement_aux.scenario_component = scenario_comp_aux
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
        msg_rspt.information.append(measurement_aux.date_acquisition)
        msg_rspt.information.append(measurement_aux.metric_id)
        msg_rspt.information.append(measurement_aux.designer_id)
        msg_rspt.information.append(measurement_aux.scenario_component_id)
        session.close()
        return msg_rspt
