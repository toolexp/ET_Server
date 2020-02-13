# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey, and_
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message


class Experimenter(Base):
    __tablename__ = 'experimenters'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, name, surname, email, password):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.name, self.surname, self.email)

    @staticmethod
    def create(parameters, session):
        """
        Creates an 'Experimenter' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable.
        :param parameters:
        :param session:
        :return:
        """
        # Received 'parameters' --> [name, surname, email, password]
        try:
            msg_rspt = Message(action=2, comment='Register created successfully')
            current_experimenter = session.query(Experimenter).filter(Experimenter.email == parameters[2]).first()
            if not current_experimenter:    # Check if email is already in use
                experimenter_aux = Experimenter(parameters[0], parameters[1], parameters[2], parameters[3])
                session.add(experimenter_aux)
                session.commit()
            else:
                msg_rspt.action = 5
                msg_rspt.comment = 'Provided email is already in use'
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error creating experimenter: ' + str(e))

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'Experimenters' registered into the DB. The list contains a string representation of
        each 'Experimenter' (__str__()).
        :param parameters:
        :param session:
        :return:
        """
        try:
            experimenters = session.query(Experimenter).all()
            session.close()
            msg_rspt = Message(action=2, information=[])
            for experimenter in experimenters:
                msg_rspt.information.append(experimenter.__str__())
            return msg_rspt
        except Exception as e:
            raise Exception('Error retrieving experimenters: ' + str(e))

    @staticmethod
    def update(parameters, session):
        """
        Updates an 'Experimenter' object from the DB, the id and new data for the object is inside the 'parameters'
        variable.
        :param parameters:
        :param session:
        :return:
        """
        # Received 'parameters' --> [id_experimenter, name, surname, email, password]
        try:
            msg_rspt = Message(action=2, comment='Register updated successfully')
            current_experimenter = session.query(Experimenter).filter(and_(Experimenter.email == parameters[3],
                                                                      Experimenter.id != parameters[0])).first()
            if not current_experimenter:    # Check if email is already in use
                experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
                experimenter_aux.name = parameters[1]
                experimenter_aux.surname = parameters[2]
                experimenter_aux.email = parameters[3]
                experimenter_aux.password = parameters[4]
                session.commit()
            else:
                msg_rspt.action = 5
                msg_rspt.comment = 'Provided email is already in use'
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error updating experimenter: ' + str(e))

    @staticmethod
    def delete(parameters, session):
        """
        Removes an 'Experimenter' object from the DB. The 'parameters' contains de id of the 'Experimenter' object.
        :param parameters:
        :param session:
        :return:
        """
        # Received 'parameters' --> [id_experimenter]
        try:
            experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
            session.delete(experimenter_aux)
            session.commit()
            session.close()
            msg_rspt = Message(action=2, comment='Register deleted successfully')
            return msg_rspt
        except Exception as e:
            raise Exception('Error removing experimenter: ' + str(e))

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of an 'Experimenter' object from the DB. The 'parameters' contains de id of
        the desired 'Experimenter'. This function can also ask for info when logging in as experimenter. Each
        attribute occupies a space of the returned list.
        :param parameters:
        :param session:
        :return:
        """
        try:
            msg_rspt = Message(action=2, information=[])
            # 1. Received 'parameters' --> [email 'login']
            if len(parameters) == 2:  # Asking for info in login form
                experimenter_aux = session.query(Experimenter).filter(Experimenter.email == parameters[0]).first()
                if not experimenter_aux:
                    return Message(action=5, information=['The experimenter is not registered in the system'],
                                   comment='Error selecting register')
                msg_rspt.information.append(experimenter_aux.id)
            # 2. Received 'parameters' --> [id_experimenter]
            else:
                experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
            msg_rspt.information.append(experimenter_aux.name)
            msg_rspt.information.append(experimenter_aux.surname)
            msg_rspt.information.append(experimenter_aux.email)
            msg_rspt.information.append(experimenter_aux.password)
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error selecting experimenter: ' + str(e))
