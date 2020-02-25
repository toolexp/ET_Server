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
    """
    A class used to represent a pattern. A pattern object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param template_id: identifier of the template object that the pattern is associated with. This is a foreign key
    :type template_id: int
    :param template: template object that the pattern is associated with
    :type template: Modules.Classes.Template.Template
    """

    __tablename__ = 'patterns'

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('templates.id'))

    template = relationship("Template", backref=backref("patterns", cascade="all, delete-orphan", single_parent=True))

    def __init__(self, template):
        """
        Constructor of the class
        """
        self.template = template

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}'.format(self.id, self.template_id)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'Pattern' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_template]
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
        """
        Retrieves a list of 'Patterns' registered into the DB. The list contains a string representation of
        each 'Pattern' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        if len(parameters) == 0:    # Asks for all patterns stored into the database
            patterns = session.query(Pattern).all()
        else:   # Asks for patterns associated with an experimental scenario and are for an specific designers group
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
        """
        Removes a 'Pattern' object from the DB. The 'parameters' contains de id of the 'Pattern' object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
        exp_scenario_aux = session.query(ExperimentalScenarioPattern).filter(ExperimentalScenarioPattern.pattern_id ==
                                                                             parameters[0]).first()
        if exp_scenario_aux:    # First check if the pattern is not associated with any experimental scenario
            return Message(action=5, information=['The pattern is associated to one or more experimental scenarios'],
                           comment='Error deleting register')
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
        expected_sols = session.query(ExpectedSolution).all()
        for item in expected_sols:  # Then, check if the pattern is not associated with any expected solution
            if pattern_aux in item.patterns:
                return Message(action=5, information=['The pattern is associated to one or more ideal solutions'],
                               comment='Error deleting register')
        sent_sols = session.query(SentSolution).all()
        for item in sent_sols:  # Finally, check if the pattern is not associated with any sent solution
            if pattern_aux in item.patterns:
                return Message(action=5, information=['The pattern is associated to one or more sent solutions'],
                               comment='Error deleting register')
        diagrams_aux = session.query(PatternSection).filter(and_(PatternSection.pattern_id == parameters[0],
                                                                 PatternSection.diagram_id != None)).all()
        for item in diagrams_aux:   # Delete diagrams (only files) that may be associated with the pattern
            Diagram.delete([item.diagram_id, 'just remove path'], session)
        session.delete(pattern_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of a 'Pattern' object from the DB. The 'parameters' contains de id of
        the desired 'Pattern'.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
        if len(parameters) == 2:    # Asks for the pattern to update its info
            from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
            exp_scenario_aux = session.query(ExperimentalScenarioPattern).\
                filter(ExperimentalScenarioPattern.pattern_id == parameters[0]).first()
            if exp_scenario_aux:    # First check if the pattern is not associated with any experimental scenario
                return Message(action=5,
                               information=['The pattern is associated to one or more experimental scenarios'],
                               comment='Error selecting register')
            expected_sols = session.query(ExpectedSolution).all()
            for item in expected_sols:  # Then, check if the pattern is not associated with any expected solution
                if pattern_aux in item.patterns:
                    return Message(action=5, information=['The pattern is associated to one or more ideal solutions'],
                                   comment='Error selecting register')
            sent_sols = session.query(SentSolution).all()
            for item in sent_sols:  # Finally, check if the pattern is not associated with any sent solution
                if pattern_aux in item.patterns:
                    return Message(action=5, information=['The pattern is associated to one or more sent solutions'],
                                   comment='Error selecting register')
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(pattern_aux.template.__str__())
        session.close()
        return msg_rspt
