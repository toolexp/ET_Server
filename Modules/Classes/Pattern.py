# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Template import Template
from Modules.Classes.PatternSection import PatternSection
from Modules.Classes.Diagram import Diagram
from Modules.Classes.ExpectedSolution import ExpectedSolution
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
        if len(parameters) == 0:
            patterns = session.query(Pattern).all()
        else:
            from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
            # Received --> [id_exp_scenario, pattern_type]
            patterns = session.query(Pattern). \
                join(ExperimentalScenarioPattern.pattern).\
                filter(and_(ExperimentalScenarioPattern.experimental_scenario_id == parameters[0],
                            ExperimentalScenarioPattern.pattern_type == parameters[1])).all()
        msg_rspt = Message(action=2, information=[])
        for pattern in patterns:
            msg_rspt.information.append(pattern.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
        exp_scenario_aux = session.query(ExperimentalScenarioPattern).filter(ExperimentalScenarioPattern.pattern_id ==
                                                                             parameters[0]).first()
        if exp_scenario_aux:
            return Message(action=5, information=['The pattern is associated to one or more experimental scenarios'],
                           comment='Error deleting register')
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
        expected_sols = session.query(ExpectedSolution).all()
        for item in expected_sols:
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
        if len(parameters) == 2:
            from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
            exp_scenario_aux = session.query(ExperimentalScenarioPattern).\
                filter(ExperimentalScenarioPattern.pattern_id == parameters[0]).first()
            if exp_scenario_aux:
                return Message(action=5,
                               information=['The pattern is associated to one or more experimental scenarios'],
                               comment='Error selecting register')
            expected_sols = session.query(ExpectedSolution).all()
            for item in expected_sols:
                if pattern_aux in item.patterns:
                    return Message(action=5, information=['The pattern is associated to one or more ideal solutions'],
                                   comment='Error selecting register')
            sent_sols = session.query(SentSolution).all()
            for item in sent_sols:
                if pattern_aux in item.patterns:
                    return Message(action=5, information=['The pattern is associated to one or more sent solutions'],
                                   comment='Error selecting register')
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(pattern_aux.template.__str__())
        session.close()
        return msg_rspt
