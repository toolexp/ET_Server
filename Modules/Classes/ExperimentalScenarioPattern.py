from sqlalchemy import Column, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Pattern import Pattern


class ExperimentalScenarioPattern(Base):
    """
    A class used to represent an association object between a pattern and an experimental scenario.
    An association object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param pattern_type: indicator of a pattern's membership type to a scenario (experimental or control)
    :type pattern_type: int
    :param pattern_id: identifier of the pattern object that belongs to the association. This is a foreign key
    :type pattern_id: int
    :param experimental_scenario_id: identifier of the experimental_scenario object that belongs to the association.
    This is a foreign key
    :type experimental_scenario_id: int
    :param pattern: pattern object that belongs to the association
    :type pattern: Module.Classes.Pattern.Pattern
    :param experimental_scenario: experimental scenario object that belongs to the association
    :type experimental_scenario: Module.Classes.ExperimentalScenario.ExperimentalScenario
    """

    __tablename__ = 'experimental_scenarios_patterns'

    id = Column(Integer, primary_key=True)
    pattern_type = Column(Integer)   # Indicates whether the pattern belongs to the control group or experimental
    # group in an specific experimental scenario
    experimental_scenario_id = Column(Integer, ForeignKey('experimental_scenarios.id'))
    pattern_id = Column(Integer, ForeignKey('patterns.id'))

    experimental_scenario = relationship("ExperimentalScenario",
                                         backref=backref("pattern_associations", cascade="all, delete-orphan"))
    pattern = relationship("Pattern", backref=backref("experimental_scenario_associations", cascade="all, delete-orphan"))

    def __init__(self, pattern_type, experimental_scenario, pattern):
        """
        Constructor of the class
        """
        self.pattern_type = pattern_type    # if pattern_type=1 --> experimental group, otherwise control group
        self.experimental_scenario = experimental_scenario
        self.pattern = pattern

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}¥{}'.format(self.id, self.pattern_type, self.experimental_scenario_id, self.pattern_id)

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'ExperimentalScenarioPattern' registered into the DB. The target objects depends of the
        length of the 'parameters'. The list contains a string representation of each 'ExperimentalScenarioPattern'
        (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 0:    # Ask for all associations stored in DB
            exp_scenarios_pat = session.query(ExperimentalScenarioPattern).all()
            for item in exp_scenarios_pat:
                msg_rspt.information.append(item.__str__())
        else:  # Ask for patterns of an experimental scenario, separated by groups
            # Received --> [id_exp_scenario]
            exp_scenarios_pat = session.query(ExperimentalScenarioPattern).filter(
                ExperimentalScenarioPattern.experimental_scenario_id == parameters[0]).all()
            exp_patterns = []
            ctrl_patterns = []
            for item in exp_scenarios_pat:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item.pattern_id).first()
                if item.pattern_type == 1:  # if pattern_type=1 --> experimental group, otherwise control group
                    exp_patterns.append(pattern_aux.__str__())
                else:
                    ctrl_patterns.append(pattern_aux.__str__())
            msg_rspt.information.append(exp_patterns)
            msg_rspt.information.append(ctrl_patterns)
        session.close()
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes all 'ExperimentalScenarioPattern' object from the DB which design type is 'experimental'. The
        'parameters' contains de id of the 'Experiment' object that contains all experimental scenarios from which
        the target 'ExperimentalScenarioPattern' objects are. This function is called only when an experiment is
        updated from 'experimental' to 'control' design type

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.ExperimentalScenario import ExperimentalScenario
        # Received --> [id_exeriment]
        # Retrieve all scenarios associated with target experiment
        exp_sc = session.query(ExperimentalScenario).filter(ExperimentalScenario.experiment_id == parameters[0]).all()
        for item in exp_sc:
            # Retrieve all ExperimentalScenarioPattern association for current experimental scenario
            exp_scenarios_pat = session.query(ExperimentalScenarioPattern).filter(and_(
                ExperimentalScenarioPattern.experimental_scenario_id == item.id,
                ExperimentalScenarioPattern.pattern_type == 2)).all()
            for item2 in exp_scenarios_pat:
                session.delete(item2)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt