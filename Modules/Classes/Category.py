# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Classification import Classification
from Modules.Classes.Section import Section

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    classification_id = Column(Integer, ForeignKey('classifications.id'))

    classification = relationship("Classification", backref=backref("categories", cascade="all, delete-orphan",
                                                                    single_parent=True))

    def __init__(self, name, classification):
        self.name = name
        self.classification = classification

    def __str__(self):
        return '{}¥{}¥{}'.format(self.id, self.name, self.classification_id)

    @staticmethod
    def create(parameters, session):
        classification_aux = session.query(Classification).filter(Classification.id == parameters[1]).first()
        category_aux = Category(parameters[0], classification_aux)
        session.add(category_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        if len(parameters) == 0:
            categories = session.query(Category).all()
        else:
            categories = session.query(Category).filter(Category.classification_id == parameters[0]).all()
        msg_rspt = Message(action=2, information=[])
        for item in categories:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
        section_aux.name = parameters[1]
        section_aux.description = parameters[2]
        section_aux.data_type = parameters[3]
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        # Received --> [id_classification]
        categories_aux = session.query(Category).filter(Category.classification_id == parameters[0]).all()
        for item in categories_aux:
            session.delete(item)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        category_aux = session.query(Category).filter(Category.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(category_aux.name)
        msg_rspt.information.append(category_aux.classification_id)
        session.close()
        return msg_rspt
