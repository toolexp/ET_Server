from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Section import Section
from Modules.Classes.TemplateSection import TemplateSection


class Template(Base):
    """
    A class used to represent a template. A template object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param name: name of the template
    :type name: str
    :param description: description of the template
    :type description: str
    :param sections: list of sections objects that the template has
    :type sections: list[Modules.Classes.Section.Section]
    """
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # sections = relationship("Section", secondary="templates_sections", backref="templates")
    sections = relationship("Section", secondary="templates_sections", viewonly=True)

    def __init__(self, name, description):
        """
        Constructor of the class
        """
        self.name = name
        self.description = description

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}'.format(self.id, self.name, self.description)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'Template' object and stores it into the DB, the data for the object is inside the
        'parameters' variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received: [name, description, [id_section1, id_section2, id_section3, ...],
        # [id_main_section_1, id_main_section_2, id_main_section_3], [mandatory_section1, mandatory_section2, ...]]
        template_aux = Template(parameters[0], parameters[1])   # Creates template
        session.add(template_aux)
        for index, item in enumerate(parameters[2]):
            section_aux = session.query(Section).filter(Section.id == item).first()
            if parameters[3][index] == '✓':
                main = True
            else:
                main = False
            if parameters[4][index] == '✓':
                mandatory = True
            else:
                mandatory = False
            # Creates association of template and section, with attributes of this association
            template_sec_aux = TemplateSection(mandatory, index + 1, main, template_aux, section_aux)
            session.add(template_sec_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'Templates' registered into the DB. The list contains a string representation of
        each 'Template' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        templates = session.query(Template).all()
        msg_rspt = Message(action=2, information=[])
        for template in templates:
            msg_rspt.information.append(template.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        """
        Updates a 'Template' object from the DB, the id and new data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received: [id_template, name, description, [id_section1, id_section2, id_section3, ...],
        # [id_main_section_1, id_main_section_2, id_main_section_3], [mandatory_section1, mandatory_section2, ...]]
        template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
        template_aux.name = parameters[1]
        template_aux.description = parameters[2]
        # Deletes existing association of template and section
        templates_secs_aux = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]).all()
        for item in templates_secs_aux:
            session.delete(item)
        for index, item in enumerate(parameters[3]):
            section_aux = session.query(Section).filter(Section.id == item).first()
            if parameters[4][index] == '✓':
                main = True
            else:
                main = False
            if parameters[5][index] == '✓':
                mandatory = True
            else:
                mandatory = False
            # Creates association of template and section, with attributes of this association
            template_sec_aux = TemplateSection(mandatory, index + 1, main, template_aux, section_aux)
            session.add(template_sec_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes a 'Template' object from the DB. The 'parameters' contains de id of the 'Template' object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.Pattern import Pattern
        pattern_aux = session.query(Pattern).filter(Pattern.template_id == parameters[0]).first()
        if pattern_aux:     # Check if template is associated with a pattern
            return Message(action=5, information=['The template is associated to one or more patterns'],
                           comment='Error deleting register')
        template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
        session.delete(template_aux)
        session.commit()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        session.close()
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of a 'Template' object from the DB. The 'parameters' contains de id of the
        desired 'Template'. Each attribute occupies a space of the returned list.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> parameters = [id_template]
        from Modules.Classes.Pattern import Pattern
        if len(parameters) == 2:    # Check if template is associated with a pattern, when updating
            pattern_aux = session.query(Pattern).filter(Pattern.template_id == parameters[0]).first()
            if pattern_aux:
                return Message(action=5, information=['The template is associated to one or more patterns'],
                               comment='Error selecting register')
        template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(template_aux.name)
        msg_rspt.information.append(template_aux.description)
        msg_rspt.information.append([])
        template_sections_aux = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]). \
            order_by(TemplateSection.position).all()
        for item in template_sections_aux:
            msg_rspt.information[2].append(item.__str__())
        session.close()
        # Return --> msg_rspt = [2, '', [template_name, template_description, [section1._str_(),
        # section2._str_(), ...]]]
        return msg_rspt
