# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.TemplateSection import TemplateSection


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    data_type = Column(String)
    classification_id = Column(Integer, ForeignKey('classifications.id'))

    classification = relationship("Classification", backref=backref("sections", cascade="all, delete-orphan",
                                                                    single_parent=True))

    def __init__(self, name='', description='', data_type='', classification=None):
        self.name = name
        self.description = description
        self.data_type = data_type
        self.classification = classification

    def __str__(self):
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.data_type, self.classification_id)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.Classification import Classification
        if len(parameters) == 4:
            classification_aux = session.query(Classification).filter(Classification.id == parameters[3]).first()
            section_aux = Section(parameters[0], parameters[1], parameters[2], classification_aux)
        else:
            section_aux = Section(parameters[0], parameters[1], parameters[2])
        session.add(section_aux)
        session.commit()
        section_aux = session.query(Section).order_by(Section.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[section_aux.__str__()], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        sections = session.query(Section).all()
        msg_rspt = Message(action=2, information=[])
        for section in sections:
            msg_rspt.information.append(section.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        from Modules.Classes.Classification import Classification
        section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
        section_aux.name = parameters[1]
        section_aux.description = parameters[2]
        section_aux.data_type = parameters[3]
        section_aux.classification = None
        if len(parameters) == 5:
            classification_aux = session.query(Classification).filter(Classification.id == parameters[4]).first()
            section_aux.classification = classification_aux
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        template_aux = session.query(TemplateSection).filter(TemplateSection.section_id == parameters[0]).first()
        if template_aux:
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
        if len(parameters) == 2:
            template_aux = session.query(TemplateSection).filter(TemplateSection.section_id == parameters[0]).first()
            if template_aux:
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


