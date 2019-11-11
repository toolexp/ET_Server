# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey, or_
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message

from Modules.Classes.ExperimentalScenario import ExperimentalScenario

designers_groups_designers_association = Table(
    'designers_groups_designers', Base.metadata,
    Column('designers_group_id', Integer, ForeignKey('designers_groups.id')),
    Column('designer_id', Integer, ForeignKey('designers.id'))
)


class DesignersGroup(Base):
    __tablename__ = 'designers_groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    designers = relationship("Designer", secondary=designers_groups_designers_association, backref='designers_groups')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, len(self.designers))

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.Designer import Designer
        designers_group_aux = DesignersGroup(parameters[0], parameters[1])
        for item in parameters[2]:
            designer_aux = session.query(Designer).filter(Designer.id == item).first()
            designers_group_aux.designers.append(designer_aux)
        session.add(designers_group_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        designers_groups = session.query(DesignersGroup).all()
        msg_rspt = Message(action=2, information=[])
        for designer_group in designers_groups:
            msg_rspt.information.append(designer_group.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        designers_group_aux = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[0]).first()
        designers_group_aux.name = parameters[1]
        designers_group_aux.description = parameters[2]
        designers_group_aux.designers = []
        for item in parameters[3]:
            designer_aux = session.query(Designer).filter(Designer.id == item).first()
            designers_group_aux.designers.append(designer_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        experimental_scenario = session.query(ExperimentalScenario).\
            filter(or_(ExperimentalScenario.control_group_id == parameters[0],
                       ExperimentalScenario.experimental_group_id == parameters[0])).first()
        if experimental_scenario:
            return Message(action=5, information=['The designers group is associated to one or more experimental scenarios'],
                           comment='Error deleting register')
        designers_group_aux = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[0]).first()
        session.delete(designers_group_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        designers_group_aux = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(designers_group_aux.name)
        msg_rspt.information.append(designers_group_aux.description)
        msg_rspt.information.append([])
        for i in range(0, len(designers_group_aux.designers)):
            msg_rspt.information[2].append(designers_group_aux.designers[i].__str__())
        session.close()
        return msg_rspt