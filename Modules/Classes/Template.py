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
        # Received: [name, description, id_visual_section, [id_section1, id_section2, id_section3, ...],
        # [mandatory_section1, mandatory_section2, ...]]
        template_aux = Template(parameters[0], parameters[1])
        session.add(template_aux)
        for index, item in enumerate(parameters[3]):
            section_aux = session.query(Section).filter(Section.id == item).first()
            if parameters[4][index] == '✓':
                mandatory = True
            else:
                mandatory = False
            if item == parameters[2]:
                visual = True
            else:
                visual = False
            template_sec_aux = TemplateSection(mandatory, index + 1, visual, template_aux, section_aux)
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
        # Received: [id_template, name, description, id_visual_section, [id_section1, id_section2, id_section3, ...],
        # [mandatory_section1, mandatory_section2, ...]]
        template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
        template_aux.name = parameters[1]
        template_aux.description = parameters[2]
        templates_secs_aux = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]).all()
        for item in templates_secs_aux:
            session.delete(item)
        for index, item in enumerate(parameters[4]):
            section_aux = session.query(Section).filter(Section.id == item).first()
            if parameters[5][index] == '✓':
                mandatory = True
            else:
                mandatory = False
            if item == parameters[3]:
                visual = True
            else:
                visual = False
            template_sec_aux = TemplateSection(mandatory, index + 1, visual, template_aux, section_aux)
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
                               comment='Error selecting register')
        # Return --> msg_rspt = [2, '', [template_name, template_description, [section1._str_(), section2._str_(), ...]]]
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
        return msg_rspt
