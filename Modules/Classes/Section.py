from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.TemplateSection import TemplateSection


class Section(Base):
    """
    A class used to represent a section of a template. A section object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param name: name of the section
    :type name: str
    :param description: description of the section
    :type description: str
    :param classification_id: identifier of the classification object which the section may be associated to.
    This is a foreign key
    :type classification_id: int
    :param classification: classification object which the section may be associated to
    :type classification: Modules.Classes.Classification.Classification
    """
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    data_type = Column(String)
    classification_id = Column(Integer, ForeignKey('classifications.id'))

    classification = relationship("Classification", backref=backref("sections", cascade="all, delete-orphan",
                                                                    single_parent=True))

    def __init__(self, name='', description='', data_type='', classification=None):
        """
        Constructor of the class
        """
        self.name = name
        self.description = description
        self.data_type = data_type
        self.classification = classification

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.data_type, self.classification_id)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'Section' object and stores it into the DB, the data for the object is inside the
        'parameters' variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.Classification import Classification
        if len(parameters) == 4:    # Creates a section that is associated with a classification
            classification_aux = session.query(Classification).filter(Classification.id == parameters[3]).first()
            section_aux = Section(parameters[0], parameters[1], parameters[2], classification_aux)
        else:   # Creates a section (text type or file type)
            section_aux = Section(parameters[0], parameters[1], parameters[2])
        session.add(section_aux)
        session.commit()
        section_aux = session.query(Section).order_by(Section.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[section_aux.__str__()], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'Sections' registered into the DB. The list contains a string representation of
        each 'Section' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        sections = session.query(Section).all()
        msg_rspt = Message(action=2, information=[])
        for section in sections:
            msg_rspt.information.append(section.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        """
        Updates a 'Section' object from the DB, the id and new data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.Classification import Classification
        section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
        section_aux.name = parameters[1]
        section_aux.description = parameters[2]
        section_aux.data_type = parameters[3]
        section_aux.classification = None
        if len(parameters) == 5:    # If section is associated with a classification
            classification_aux = session.query(Classification).filter(Classification.id == parameters[4]).first()
            section_aux.classification = classification_aux
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes a 'Section' object from the DB. The 'parameters' contains de id of the 'Section' object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        template_aux = session.query(TemplateSection).filter(TemplateSection.section_id == parameters[0]).first()
        if template_aux:    # Check if a section is associated with a template
            return Message(action=5, information=['The section is associated to one or more templates'],
                           comment='Error deleting register')
        section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
        session.delete(section_aux)
        session.commit()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        session.close()
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of a 'Section' object from the DB. The 'parameters' contains de id of the
        desired 'Section'. Each attribute occupies a space of the returned list.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        if len(parameters) == 2:    # When selecting a section to update it
            template_aux = session.query(TemplateSection).filter(TemplateSection.section_id == parameters[0]).first()
            if template_aux:    # Check if a section is associated with a template
                return Message(action=5, information=['The section is associated to one or more templates'],
                               comment='Error selecting register')
        section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(section_aux.name)
        msg_rspt.information.append(section_aux.description)
        msg_rspt.information.append(section_aux.data_type)
        msg_rspt.information.append(section_aux.classification_id)
        session.close()
        return msg_rspt


