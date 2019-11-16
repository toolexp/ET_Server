# coding=utf-8

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Section import Section
from Modules.Classes.TemplateSection import TemplateSection


class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    # sections = relationship("Section", secondary="templates_sections", backref="templates")
    sections = relationship("Section", secondary="templates_sections", viewonly=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return '{}¥{}¥{}'.format(self.id, self.name, self.description)

    @staticmethod
    def create(parameters, session):
        template_aux = Template(parameters[0], parameters[1])
        session.add(template_aux)
        for i in range(0, len(parameters[2])):
            section_aux = session.query(Section).filter(Section.id == parameters[2][i]).first()
            if parameters[3][i] == '✓':
                mandatory = True
            else:
                mandatory = False
            template_sec_aux = TemplateSection(mandatory, i + 1, template_aux, section_aux)
            session.add(template_sec_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

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
        template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
        template_aux.name = parameters[1]
        template_aux.description = parameters[2]
        templates_secs_aux = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]).all()
        for i in range(0, len(templates_secs_aux)):
            session.delete(templates_secs_aux[i])
        for i in range(0, len(parameters[3])):
            section_aux = session.query(Section).filter(Section.id == parameters[3][i]).first()
            if parameters[4][i] == '✓':
                mandatory = True
            else:
                mandatory = False
            template_sec_aux = TemplateSection(mandatory, i + 1, template_aux, section_aux)
            session.add(template_sec_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        from Modules.Classes.Pattern import Pattern
        pattern_aux = session.query(Pattern).filter(Pattern.template_id == parameters[0]).first()
        if pattern_aux:
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
        # Received --> parameters = [id_template]
        from Modules.Classes.Pattern import Pattern
        if len(parameters) == 2:
            pattern_aux = session.query(Pattern).filter(Pattern.template_id == parameters[0]).first()
            if pattern_aux:
                return Message(action=5, information=['The template is associated to one or more patterns'],
                               comment='Error deleting register')
        # Return --> msg_rspt = [2, '', [template_name, template_description, [section1._str_(), section2._str_(), ...]]]
        template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(template_aux.name)
        msg_rspt.information.append(template_aux.description)
        msg_rspt.information.append([])
        template_sections_aux = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]). \
            order_by(TemplateSection.position).all()
        for i in range(0, len(template_sections_aux)):
            msg_rspt.information[2].append(template_sections_aux[i].__str__())
        session.close()
        return msg_rspt
