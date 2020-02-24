from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message


class TemplateSection(Base):
    """
    A class used to represent an association object between a template and a section.
    An association object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param mandatory: indicator of obligation of fulfillment of a section in a template
    :type mandatory: bool
    :param position: indicator of the position of a section in a template
    :type position: int
    :param main: indicator of main section in a template (visual). There is a maximum of three main sections per template
    :type main: bool
    :param template_id: identifier of the template object that belongs to the association. This is a foreign key
    :type template_id: int
    :param section_id: identifier of the section object that belongs to the association. This is a foreign key
    :type section_id: int
    :param template: template object that belongs to the association
    :type template: Module.Classes.Template.Template
    :param section: section object that belongs to the association
    :type section: Module.Classes.Section.Section
    """
    __tablename__ = 'templates_sections'

    id = Column(Integer, primary_key=True)
    mandatory = Column(Boolean)
    position = Column(Integer)
    main = Column(Boolean)    # This field indicates if the section is allowed to be shown as main respresentation of
    # the template
    template_id = Column(Integer, ForeignKey('templates.id'))
    section_id = Column(Integer, ForeignKey('sections.id'))

    template = relationship("Template", backref=backref("section_associations", cascade="all, delete-orphan"))
    section = relationship("Section", backref=backref("template_associations", cascade="all, delete-orphan"))

    def __init__(self, mandatory, position, main, template, section):
        """
        Constructor of the class
        """
        self.mandatory = mandatory
        self.position = position
        self.main = main
        self.template = template
        self.section = section

    def __str__(self):
        """
        Method that represents the object as a string
        """
        if self.mandatory:
            aux_mand = '✓'
        else:
            aux_mand = ''
        if self.main:
            aux_main = '✓'
        else:
            aux_main = ''
        return '{}¥{}¥{}¥{}¥{}¥{}¥{}¥{}¥{}¥{}'.format(self.id, self.template_id, self.section_id, self.section.name,
                                                      self.section.description, self.section.data_type, self.position,
                                                      aux_mand, aux_main, self.section.classification_id)

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'TemplateSection' registered into the DB. The target objects depends of the
        length of the 'parameters'. The list contains a string representation of each 'TemplateSection'
        (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        if len(parameters) == 0:    # Ask for all association objects
            template_sections = session.query(TemplateSection).all()
        else:   # Ask for all association objects corresponding to a specific template
            template_sections = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]). \
                order_by(TemplateSection.position).all()
        msg_rspt = Message(action=2, information=[])
        for item in template_sections:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt
