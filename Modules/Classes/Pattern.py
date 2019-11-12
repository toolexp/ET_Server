# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Template import Template
from Modules.Classes.DesignersGroup import DesignersGroup
from Modules.Classes.PatternSection import PatternSection
from Modules.Classes.Diagram import Diagram
from Modules.Classes.ScenarioComponentPattern import ScenarioComponentPattern
from Modules.Classes.IdealSolution import IdealSolution
from Modules.Classes.SentSolution import SentSolution

class Pattern(Base):
    __tablename__ = 'patterns'

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('templates.id'))

    template = relationship("Template", backref=backref("patterns", cascade="all, delete-orphan", single_parent=True))

    def __init__(self, template):
        self.template = template

    def __str__(self):
        return '{}¥{}'.format(self.id, self.template_id)

    @staticmethod
    def create(parameters, session):
        # Received --> [id_template]
        # Returned --> [id_pattern (new)]
        template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
        pattern_aux = Pattern(template_aux)
        session.add(pattern_aux)
        session.commit()
        new_pattern_aux = session.query(Pattern).order_by(Pattern.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[new_pattern_aux.id], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        from Modules.Classes.ScenarioComponent import ScenarioComponent
        from Modules.Classes.Designer import Designer
        if len(parameters) == 0:
            patterns = session.query(Pattern).all()
        else:
            # Received --> [id_scenario_comp, pattern_type]
            patterns = session.query(Pattern). \
                join(ScenarioComponentPattern.pattern).\
                filter(and_(ScenarioComponentPattern.scenario_component_id == parameters[0],
                            ScenarioComponentPattern.pattern_type == parameters[1])).all()
        msg_rspt = Message(action=2, information=[])
        for pattern in patterns:
            msg_rspt.information.append(pattern.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        # Received --> [id_pattern, name]
        # Template can not be updated
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
        pattern_aux.name = parameters[1]
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        scenario_comp_aux = session.query(ScenarioComponentPattern).filter(ScenarioComponentPattern.pattern_id ==
                                                                           parameters[0]).first()
        if scenario_comp_aux:
            return Message(action=5, information=['The pattern is associated to one or more experimental scenarios'],
                           comment='Error deleting register')
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
        ideal_sols = session.query(IdealSolution).all()
        for item in ideal_sols:
            if pattern_aux in item.patterns:
                return Message(action=5, information=['The pattern is associated to one or more ideal solutions'],
                               comment='Error deleting register')
        sent_sols = session.query(SentSolution).all()
        for item in sent_sols:
            if pattern_aux in item.patterns:
                return Message(action=5, information=['The pattern is associated to one or more sent solutions'],
                               comment='Error deleting register')
        diagrams_aux = session.query(PatternSection).filter(and_(PatternSection.pattern_id == parameters[0],
                                                                 PatternSection.diagram_id != None)).all()
        for item in diagrams_aux:
            Diagram.delete([item.diagram_id, 'just remove path'], session)
        session.delete(pattern_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(pattern_aux.name)
        msg_rspt.information.append(pattern_aux.template.__str__())
        '''if pattern_aux.diagram is not None:
            msg_rspt.information.append(pattern_aux.diagram.__str__())'''
        session.close()
        return msg_rspt
