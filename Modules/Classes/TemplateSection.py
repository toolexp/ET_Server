# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message


class TemplateSection(Base):
    __tablename__ = 'templates_sections'

    id = Column(Integer, primary_key=True)
    mandatory = Column(Boolean)
    position = Column(Integer)
    main = Column(Boolean)    # This field indicates if the section is allowed to be shown as main respresentation of the template
    template_id = Column(Integer, ForeignKey('templates.id'))
    section_id = Column(Integer, ForeignKey('sections.id'))

    template = relationship("Template", backref=backref("section_associations", cascade="all, delete-orphan"))
    section = relationship("Section", backref=backref("template_associations", cascade="all, delete-orphan"))

    def __init__(self, mandatory, position, main, template, section):
        self.mandatory = mandatory
        self.position = position
        self.main = main
        self.template = template
        self.section = section

    def __str__(self):
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
        if len(parameters) == 0:
            template_sections = session.query(TemplateSection).all()
        else:
            template_sections = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]). \
                order_by(TemplateSection.position).all()
        msg_rspt = Message(action=2, information=[])
        for item in template_sections:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt
