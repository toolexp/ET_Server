# coding=utf-8

from sqlalchemy import Column, String, Integer, and_
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
from Modules.Classes.Measurement import Measurement


class Designer(Base):
    __tablename__ = 'designers'

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
        Creates a 'Designer' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable.
        :param parameters:
        :param session:
        :return:
        """
        # Received 'parameters' --> [name, surname, email, password]
        try:
            msg_rspt = Message(action=2, comment='Register created successfully')
            current_designers = session.query(Designer).filter(Designer.email == parameters[2]).first()
            if not current_designers:   # Check if email is already in use
                designer_aux = Designer(parameters[0], parameters[1], parameters[2], parameters[3])
                session.add(designer_aux)
                session.commit()
            else:
                msg_rspt.action = 5
                msg_rspt.comment = 'Provided email is already in use'
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error creating designer: ' + str(e))

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'Designers' registered into the DB. The list contains a string representation of
        each 'Designer' (__str__()).
        :param parameters:
        :param session:
        :return:
        """
        try:
            designers = session.query(Designer).all()
            session.close()
            msg_rspt = Message(action=2, information=[])
            for designer in designers:
                msg_rspt.information.append(designer.__str__())
            return msg_rspt
        except Exception as e:
            raise Exception('Error retrieving designers: ' + str(e))

    @staticmethod
    def update(parameters, session):
        """
        Updates a 'Designer' object from the DB, the id and new data for the object is inside the 'parameters'
        variable.
        :param parameters:
        :param session:
        :return:
        """
        # Received 'parameters' --> [id_designer, name, surname, email, password]
        try:
            msg_rspt = Message(action=2, comment='Register updated successfully')
            current_designers = session.query(Designer).filter(and_(Designer.email == parameters[3],
                                                                    Designer.id != parameters[0])).first()
            if not current_designers:   # Check if email is already in use
                designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
                designer_aux.name = parameters[1]
                designer_aux.surname = parameters[2]
                designer_aux.email = parameters[3]
                designer_aux.password = parameters[4]
                session.commit()
            else:
                msg_rspt.action = 5
                msg_rspt.comment = 'Provided email is already in use'
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error updating designer: ' + str(e))

    @staticmethod
    def delete(parameters, session):
        """
        Removes a 'Designer' object from the DB. The 'parameters' contains de id of the 'Designer' object.
        :param parameters:
        :param session:
        :return:
        """
        # Received 'parameters' --> [id_designer]
        try:
            designer_exp_aux = session.query(DesignerExperimentalScenario).\
                filter(DesignerExperimentalScenario.designer_id == parameters[0]).first()
            if designer_exp_aux:   # Check if designer is not associated in any experiment, if so, it can not be deleted
                return Message(action=5, information=['The designer is associated to one or more experimental scenarios'],
                               comment='Error deleting register')
            measurement_aux = session.query(Measurement).filter(Measurement.designer_id == parameters[0]).first()
            if measurement_aux:
                return Message(action=5, information=['The designer is associated to one or more measurements'],
                               comment='Error deleting register')
            designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
            session.delete(designer_aux)
            session.commit()
            session.close()
            msg_rspt = Message(action=2, comment='Register deleted successfully')
            return msg_rspt
        except Exception as e:
            raise Exception('Error removing designer: ' + str(e))

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of a 'Designer' object from the DB. The 'parameters' contains de id of
        the desired 'Designer'. This function can also ask for info when logging in as designer. Each attribute
        occupies a space of the returned list.
        :param parameters:
        :param session:
        :return:
        """
        try:
            msg_rspt = Message(action=2, information=[])
            # 1. Received 'parameters' --> [email 'login']
            if len(parameters) == 2:  # Asking for info in login form
                designer_aux = session.query(Designer).filter(Designer.email == parameters[0]).first()
                if not designer_aux:
                    return Message(action=5, information=['The designer is not registered in the system'],
                                   comment='Error selecting register')
                msg_rspt.information.append(designer_aux.id)
            # 2. Received 'parameters' --> [id_designer]
            else:
                designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
            msg_rspt.information.append(designer_aux.name)
            msg_rspt.information.append(designer_aux.surname)
            msg_rspt.information.append(designer_aux.email)
            msg_rspt.information.append(designer_aux.password)
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error selecting designer: ' + str(e))

