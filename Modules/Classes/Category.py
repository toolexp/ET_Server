# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Classification import Classification


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
        """
        Creates a 'Category' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable.
        :param parameters:
        :param session:
        :return:
        """
        # Received 'parameters' --> [name, id_classification]
        classification_aux = session.query(Classification).filter(Classification.id == parameters[1]).first()
        category_aux = Category(parameters[0], classification_aux)
        session.add(category_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'Categories' registered into the DB. The target objects depends of the length of the
        'parameters'. The list contains a string representation of each 'Category' (__str__()).
        :param parameters:
        :param session:
        :return:
        """
        if len(parameters) == 0:    # Ask for all categories stored in DB
            categories = session.query(Category).all()
        # Received 'parameters' --> [id_classification]
        else:   # Ask only for categories associated with a 'Classification' object
            categories = session.query(Category).filter(Category.classification_id == parameters[0]).all()
        msg_rspt = Message(action=2, information=[])
        for item in categories:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes a 'Category' object from the DB. The 'parameters' contains de id of the 'Classification' object that the
        categories are associated with.
        :param parameters:
        :param session:
        :return:
        """
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
        """
        Retrieve information (attributes) of a 'Category' object from the DB. The 'parameters' contains de id of the
        desired 'Category'. Each attribute occupies a space of the returned list.
        :param parameters:
        :param session:
        :return:
        """
        # Received --> [id_category]
        category_aux = session.query(Category).filter(Category.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(category_aux.name)
        msg_rspt.information.append(category_aux.classification_id)
        session.close()
        return msg_rspt
