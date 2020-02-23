from datetime import datetime
from os import remove
from sqlalchemy import Column, String, Integer
from Modules.Config.base import Base
from Modules.Config.Data import Message


class Diagram(Base):
    """
    A class used to represent a diagram. A diagram object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param name: diagram name (filename)
    :type name: str
    :param file_path: full path of the file (diagram) stored in the server
    :type file_path: str
    """
    __tablename__ = 'diagrams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_path = Column(String)

    def __init__(self, name, file_path):
        """
        Constructor of the class
        """
        self.name = name
        self.file_path = file_path

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}'.format(self.id, self.name, self.file_path)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'Diagram' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable. Creates a diagram into the file system.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received 'parameters' --> [file_bytes, filename, diagram_type]
        try:
            if parameters[2] == 'pattern':
                path = './Resources/Diagrams/Patterns/'
            elif parameters[2] == 'exp sol':
                path = './Resources/Diagrams/ExpectedSolution/'
            elif parameters[2] == 'sent sol':
                path = './Resources/Diagrams/SentSolutions/'
            elif parameters[2] == 'scen context':
                path = './Resources/Diagrams/ContextDiagram/'
            else:
                path = './Resources/Diagrams/'
            file = path + datetime.now().strftime("%Y%m%d_%H%M%S") + parameters[1]
            myfile = open(file, 'wb')
            myfile.write(parameters[0])
            myfile.close()
            diagram_aux = Diagram(parameters[1], file)
            session.add(diagram_aux)
            session.commit()
            new_diagram_aux = session.query(Diagram).order_by(Diagram.id.desc()).first()
            session.close()
            msg_rspt = Message(action=2, information=[new_diagram_aux.id], comment='Register created successfully')
            return msg_rspt
        except Exception as e:
            raise Exception('Error creating a diagram: ' + str(e))

    @staticmethod
    def update(parameters, session):
        """
        Updates a 'Diagram' object from the DB, the id and new data for the object is inside the 'parameters'
        variable. Removes the existing diagram from the file system and creates a new diagram.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received 'parameters' --> [id_diagram, file_bytes, filename, diagram_type]
        if parameters[3] == 'pattern':
            path = './Resources/Diagrams/Patterns/'
        elif parameters[3] == 'exp sol':
            path = './Resources/Diagrams/ExpectedSolutions/'
        elif parameters[3] == 'sent sol':
            path = './Resources/Diagrams/SentSolutions/'
        elif parameters[3] == 'scen context':
            path = './Resources/Diagrams/ContextDiagram/'
        else:
            path = './Resources/Diagrams/'
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
        remove(diagram_aux.file_path)
        file = path + parameters[2]
        myfile = open(file, 'wb')
        myfile.write(parameters[1])
        myfile.close()
        diagram_aux.name = parameters[2]
        diagram_aux.file_path = file
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes a 'Diagram' object from the DB. The 'parameters' contains de id of the 'Diagram' object. It also removes
        the diagram from the file system

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received 'parameters' --> [id_diagram]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
        remove(diagram_aux.file_path)
        if len(parameters) == 1:
            session.delete(diagram_aux)
            session.commit()
            session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of a 'Diagram' object from the DB. The 'parameters' contains de id of
        the desired 'Diagram'. Each attribute occupies a space of the returned list.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received 'parameters' --> [id_diagram]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
        myfile = open(diagram_aux.file_path, 'rb')
        file_bytes = myfile.read()
        myfile.close()
        file_name = diagram_aux.name
        session.close()
        msg_rspt = Message(action=2, information=[file_name, file_bytes], comment='Register created successfully')
        return msg_rspt
