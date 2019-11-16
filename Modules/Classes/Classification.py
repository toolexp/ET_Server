# coding=utf-8

from sqlalchemy import Column, String, Integer

from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Section import Section


class Classification(Base):
    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{}¥{}¥{}'.format(self.id, self.name, len(self.categories))

    @staticmethod
    def create(parameters, session):
        classification_aux = Classification(parameters[0])
        session.add(classification_aux)
        session.commit()
        classification_aux = session.query(Classification).order_by(Classification.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[classification_aux.id], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        classifications = session.query(Classification).all()
        msg_rspt = Message(action=2, information=[])
        for item in classifications:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        classification_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
        classification_aux.name = parameters[1]
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        section_aux = session.query(Section).filter(Section.classification_id == parameters[0]).first()
        if section_aux:
            return Message(action=5, information=['The classification is associated to one or more sections'],
                           comment='Error deleting register')
        classification_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
        session.delete(classification_aux)
        session.commit()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        session.close()
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        if len(parameters) == 2:
            section_aux = session.query(Section).filter(Section.classification_id == parameters[0]).first()
            if section_aux:
                return Message(action=5, information=['The classification is associated to one or more sections'],
                               comment='Error selecting register')
        classification_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(classification_aux.name)
        msg_rspt.information.append([])
        for item in classification_aux.categories:
            msg_rspt.information[1].append(item.__str__())
        session.close()
        return msg_rspt