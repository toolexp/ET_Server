# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Category import Category
from Modules.Classes.Diagram import Diagram

from Modules.Classes.TemplateSection import TemplateSection


class PatternSection(Base):
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
        self.content = content
        self.pattern = pattern
        self.temp_section = temp_section
        self.diagram = diagram
        self.category = category

    def __str__(self):
        return '{}¥{}¥{}¥{}¥{}¥{}'.format(self.id, self.content, self.pattern_id, self.temp_section_id, self.diagram_id,
                                          self.category_id)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.Pattern import Pattern
        # Received --> [content, id_pattern, id_temp_section, id_diagram, id_category]
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[1]).first()
        template_section_aux = session.query(TemplateSection).filter(TemplateSection.id == parameters[2]).first()
        if parameters[3] is not None:
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
        else:
            diagram_aux = None
        if parameters[4] is not None:
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
        if len(parameters) == 0:
            contents = session.query(PatternSection).all()
        elif len(parameters) == 1:
            # Received --> [id_Pattern]
            contents = session.query(PatternSection).filter(PatternSection.pattern_id == parameters[0]).all()
        else:
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
        # Received --> [id_pattern_section, content, id_diagram, id_category]
        content_aux = session.query(PatternSection).filter(PatternSection.id == parameters[0]).first()
        if parameters[2] is not None:
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
        else:
            diagram_aux = None
        if parameters[3] is not None:
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

    @staticmethod
    def delete(parameters, session):
        # Received --> [id_pattern_section]
        content_aux = session.query(PatternSection).filter(PatternSection.id == parameters[0]).first()
        session.delete(content_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt