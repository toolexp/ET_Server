from sqlalchemy import Column, String, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Category import Category
from Modules.Classes.Diagram import Diagram
from Modules.Classes.TemplateSection import TemplateSection


class PatternSection(Base):
    """
    A class used to represent a pattern section (content of a section in a pattern). A pattern section object has
    attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param content: text content of the section in the pattern
    :type content: str
    :param pattern_id: identifier of the pattern object from which the pattern section is part of. This is a foreign key
    :type pattern_id: int
    :param temp_section_id: identifier of the template section association object that the pattern section is associated
    with. This is a foreign key
    :type temp_section_id: int
    :param diagram_id: identifier of the diagram object that the pattern section is associated with. This is a foreign
    key
    :type diagram_id: int
    :param category_id: identifier of the category object that the pattern section is associated with. This is a
    foreign key
    :type category_id: int
    :param pattern: pattern object from which the pattern section is part of
    :type pattern: Modules.Classes.Pattern.Pattern
    :param temp_section: template section association object that the pattern section is associated with
    :type temp_section: Modules.Classes.TemplateSection.TemplateSection
    :param diagram: diagram object that the pattern section is associated with
    :type diagram: Modules.Classes.Diagram.Diagram
    :param category: category object that the pattern section is associated with
    :type category: Modules.Classes.Category.Category
    """
    __tablename__ = 'pattern_sections'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    pattern_id = Column(Integer, ForeignKey('patterns.id'))
    temp_section_id = Column(Integer, ForeignKey('templates_sections.id'))
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    pattern = relationship("Pattern", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                      single_parent=True))
    temp_section = relationship("TemplateSection", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                                   single_parent=True))
    diagram = relationship("Diagram", backref="pattern_section", cascade="all, delete-orphan", single_parent=True,
                           uselist=False)
    category = relationship("Category", backref=backref("pattern_sections", cascade="all, delete-orphan",
                                                        single_parent=True))

    def __init__(self, content='', pattern=None, temp_section=None, diagram=None, category=None):
        """
        Constructor of the class
        """
        self.content = content
        self.pattern = pattern
        self.temp_section = temp_section
        self.diagram = diagram
        self.category = category

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}¥{}¥{}¥{}'.format(self.id, self.content, self.pattern_id, self.temp_section_id, self.diagram_id,
                                          self.category_id)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'PatternSection' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable. Attributtes of the object will be fulfilled depending on the data type of the section, the others
        will be set to NULL

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.Pattern import Pattern
        # Received --> [content, id_pattern, id_temp_section, id_diagram, id_category]
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[1]).first()
        template_section_aux = session.query(TemplateSection).filter(TemplateSection.id == parameters[2]).first()
        if parameters[3] is not None:   # If pattern section has a diagram
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
        else:
            diagram_aux = None
        if parameters[4] is not None:   # If pattern section has a category
            category_aux = session.query(Category).filter(Category.id == parameters[4]).first()
        else:
            category_aux = None
        content_aux = PatternSection(parameters[0], pattern_aux, template_section_aux, diagram_aux, category_aux)
        session.add(content_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'PatternSections' registered into the DB. The list contains a string representation of
        each 'PatternSection' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_pattern, id_temp_section]
        contents = session.query(PatternSection).filter(and_(PatternSection.pattern_id == parameters[0],
                                                             PatternSection.temp_section_id == parameters[1])).all()
        msg_rspt = Message(action=2, information=[])
        for item in contents:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        """
        Updates a 'PatternSection' object from the DB, the id and new data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_pattern_section, content, id_diagram, id_category]
        content_aux = session.query(PatternSection).filter(PatternSection.id == parameters[0]).first()
        if parameters[2] is not None:   # If pattern section has a diagram
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
        else:
            diagram_aux = None
        if parameters[3] is not None:   # If pattern section has a category
            category_aux = session.query(Category).filter(Category.id == parameters[3]).first()
        else:
            category_aux = None
        content_aux.content = parameters[1]
        content_aux.diagram = diagram_aux
        content_aux.category = category_aux
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt