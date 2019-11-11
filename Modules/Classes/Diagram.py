# coding=utf-8

from datetime import datetime
from os import remove
from sqlalchemy import Column, String, Integer
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Template import Template



class Diagram(Base):
    __tablename__ = 'diagrams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    file_path = Column(String)

    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path

    def __str__(self):
        return '{}¥{}¥{}'.format(self.id, self.name, self.file_path)

    @staticmethod
    def create(parameters, session):
        """
           Creates a 'Diagram' object and stores it into the DB, the data for the
           object is inside the 'parameters'

           Parameters
           ----------
           parameters: Message.information [string, string, string, string]
               -> parameters[0] has Bytes: file content
               -> parameters[1] has string: filename
           session: Session
               Session of connection with the database

           Returns
           -------
           msg_rspt: Message
               Message with information of the fail or success of the operation and the id of the
               created register

           Raises
           ------
           Exception:
               If any of the lines of code generates an error
           """
        try:
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
    def read(parameters, session):
        templates = session.query(Template).all()
        msg_rspt = Message(action=2, information=[])
        for template in templates:
            msg_rspt.information.append(template.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        # Received --> [id_diagram, file_content, filename]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
        remove(diagram_aux.file_path)
        path = './Resources/Diagrams/'
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
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
        myfile = open(diagram_aux.file_path, 'rb')
        file_bytes = myfile.read()
        myfile.close()
        file_name = diagram_aux.name
        session.close()
        msg_rspt = Message(action=2, information=[file_name, file_bytes], comment='Register created successfully')
        return msg_rspt
