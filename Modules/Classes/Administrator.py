# coding=utf-8

from sqlalchemy import Column, String, Integer, and_
from Modules.Config.base import Base
from Modules.Config.Data import Message


class Administrator(Base):
    __tablename__ = 'administrators'

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
       Creates an 'Administrator' object and stores it into the DB, the data for the
       object is inside the 'parameters'

       Parameters
       ----------
       parameters: Message.information [string, string, string, string]
           -> parameters[0] has Administrator.name
           -> parameters[1] has Administrator.surname
           -> parameters[2] has Administrator.email
           -> parameters[3] has Administrator.password
       session: Session
           Session of connection with the database

       Returns
       -------
       msg_rspt: Message
           Message with information of the fail or success of the operation

       Raises
       ------
       Exception:
           If any of the lines of code generates an error
       """
        try:
            # Check if username is available
            msg_rspt = Message(action=2, comment='Register created successfully')
            current_admin = session.query(Administrator).filter(Administrator.email == parameters[2]).first()
            if not current_admin:
                admin_aux = Administrator(parameters[0], parameters[1], parameters[2], parameters[3])
                session.add(admin_aux)
                session.commit()
            else:
                msg_rspt.action = 5
                msg_rspt.comment = 'Provided email is already in use'
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error creating administrator: ' + str(e))

    @staticmethod
    def read(parameters, session):
        """
            Retreive a list with al the 'Administrators' registered into the DB. The list
            contains a string representation of each 'Administrator' (__str__())

            Parameters
            ----------
            parameters: Message.information [] (not used)
            session: Session
                Session of connection with the database

            Returns
            -------
            msg_rspt: Message
                Message with the list of administrators

            Raises
            ------
            Exception:
                If any of the lines of code generates an error
            """
        try:
            admins = session.query(Administrator).all()
            session.close()
            msg_rspt = Message(action=2, information=[])
            for admin in admins:
                msg_rspt.information.append(admin.__str__())
            return msg_rspt
        except Exception as e:
            raise Exception('Error retrieving administrators: ' + str(e))

    @staticmethod
    def update(parameters, session):
        """
            Update information of an 'Administrator' registered into the DB.

            Parameters
            ----------
            parameters: Message.information [int, string, string, string, string]
               -> parameters[0] has Administrator.id
               -> parameters[1] has Administrator.name
               -> parameters[2] has Administrator.surname
               -> parameters[3] has Administrator.email
               -> parameters[4] has Administrator.password
            session: Session
                Session of connection with the database

            Returns
            -------
            msg_rspt: Message
                Message with information of the fail or success of the operation

            Raises
            ------
            Exception:
                If any of the lines of code generates an error
            """
        try:
            msg_rspt = Message(action=2, comment='Register updated successfully')
            current_admin = session.query(Administrator).filter(and_(Administrator.email == parameters[3],
                                                                     Administrator.id != parameters[0])).first()
            if not current_admin:
                admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
                admin_aux.name = parameters[1]
                admin_aux.surname = parameters[2]
                admin_aux.email = parameters[3]
                admin_aux.password = parameters[4]
                session.commit()
            else:
                msg_rspt.action = 5
                msg_rspt.comment = 'Provided email is already in use'
            session.close()
            return msg_rspt
        except Exception as e:
            raise Exception('Error updating administrator: ' + str(e))

    @staticmethod
    def delete(parameters, session):
        """
            Remove an 'Administrator' from the DB.

            Parameters
            ----------
            parameters: Message.information [int]
               -> parameters[0] has Administrator.id
            session: Session
                Session of connection with the database

            Returns
            -------
            msg_rspt: Message
                Message with information of the fail or success of the operation

            Raises
            ------
            Exception:
                If any of the lines of code generates an error
            """
        try:
            admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
            session.delete(admin_aux)
            session.commit()
            session.close()
            msg_rspt = Message(action=2, comment='Register deleted successfully')
            return msg_rspt
        except Exception as e:
            raise Exception('Error removing administrator: ' + str(e))

    @staticmethod
    def select(parameters, session):
        """
            Retrieve information of an 'Administrator' from the DB.

            Parameters
            ----------
            parameters: Message.information [int]
               -> parameters[0] has Administrator.id
            session: Session
                Session of connection with the database

            Returns
            -------
            msg_rspt: Message
                Message with information of the 'Administrator'

            Raises
            ------
            Exception:
                If any of the lines of code generates an error
            """
        try:
            msg_rspt = Message(action=2, information=[])
            if len(parameters) == 1:
                admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
            else:  # Asking for info in login form
                admin_aux = session.query(Administrator).filter(Administrator.email == parameters[0]).first()
                if not admin_aux:
                    return Message(action=5, information=['The administrator is not registered in the system'],
                                   comment='Error selecting register')
                msg_rspt.information.append(admin_aux.id)
            msg_rspt.information.append(admin_aux.name)
            msg_rspt.information.append(admin_aux.surname)
            msg_rspt.information.append(admin_aux.email)
            msg_rspt.information.append(admin_aux.password)
            return msg_rspt
        except Exception as e:
            raise Exception('Error selecting administrator: ' + str(e))

