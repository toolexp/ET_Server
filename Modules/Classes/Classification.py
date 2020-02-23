from sqlalchemy import Column, String, Integer

from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Section import Section


class Classification(Base):
    """
    A class used to represent a classification. A classification object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param name: name of the classification
    :type name: str
    """

    __tablename__ = 'classifications'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        """
        Constructor of the class
        """
        self.name = name

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}'.format(self.id, self.name, len(self.categories))

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'Classification' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable. It also returns the id of the newly created object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received 'parameters' --> [name]
        classification_aux = Classification(parameters[0])
        session.add(classification_aux)
        session.commit()
        classification_aux = session.query(Classification).order_by(Classification.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[classification_aux.id], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'Classifications' registered into the DB. The list contains a string representation of each
        'Category' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        classifications = session.query(Classification).all()
        msg_rspt = Message(action=2, information=[])
        for item in classifications:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        """
        Updates a 'Classification' object from the DB, the id and new data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received 'parameters' --> [id_classification, name]
        classification_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
        classification_aux.name = parameters[1]
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes a 'Classification' object from the DB. The 'parameters' contains de id of the 'Classification' object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received 'parameters' --> [id_classification]
        section_aux = session.query(Section).filter(Section.classification_id == parameters[0]).first()
        if section_aux:  # If a classification is being used by a section, it can not be deleted
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
        """
        Retrieve information (attributes) of a 'Classification' object from the DB. The 'parameters' contains de id of the
        desired 'Classification'. Each attribute occupies a space of the returned list.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # 1. Received 'parameters' --> [id_classification 'validate']
        if len(parameters) == 2:    # When selecting a classification to update it, first must validate is not being
            # used by any section
            section_aux = session.query(Section).filter(Section.classification_id == parameters[0]).first()
            if section_aux:
                return Message(action=5, information=['The classification is associated to one or more sections'],
                               comment='Error selecting register')
        # 2. Received 'parameters' --> [id_classification]
        classification_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(classification_aux.name)
        msg_rspt.information.append([])
        for item in classification_aux.categories:
            msg_rspt.information[1].append(item.__str__())
        session.close()
        return msg_rspt