from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Diagram import Diagram
from Modules.Classes.ExperimentalScenario import ExperimentalScenario
from Modules.Classes.ExpectedSolution import ExpectedSolution


class Problem(Base):
    """
    A class used to represent a problem. A problem object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param brief_description: short description of the problem (like name of the problem)
    :type brief_description: str
    :param description: description of the problem
    :type description: str
    :param expected_solution_id: identifier of the expected solution object that the problem is associated with.
    This is a foreign key
    :type expected_solution_id: int
    :param experimental_scenario_id: identifier of the experimental scenario object that the problem is associated with.
    This is a foreign key
    :type experimental_scenario_id: int
    :param expected_solution: expected solution object that the problem is associated with
    :type expected_solution: Modules.Classes.ExpectedSolution.ExpectedSolution
    :param experimental_scenario: experimental scenario object that the problem is associated with
    :type experimental_scenario: Modules.Classes.ExperimentalScenario.ExperimentalScenario
    """
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    brief_description = Column(String)
    description = Column(String)
    expected_solution_id = Column(Integer, ForeignKey('expected_solutions.id'))
    experimental_scenario_id = Column(Integer, ForeignKey('experimental_scenarios.id'))

    expected_solution = relationship("ExpectedSolution", backref="problem", cascade="all, delete-orphan",
                                     single_parent=True, uselist=False)
    experimental_scenario = relationship("ExperimentalScenario", backref=backref("problems", cascade="all, delete-orphan"))

    def __init__(self, brief_description, description, expected_solution, experimental_scenario):
        """
        Constructor of the class
        """
        self.brief_description = brief_description
        self.description = description
        self.expected_solution = expected_solution
        self.experimental_scenario = experimental_scenario

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.brief_description, self.description, self.expected_solution_id,
                                       self.experimental_scenario_id)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'Problem' object and stores it into the DB, the data for the object is inside the 'parameters'
        variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [brief_description, description, id_expected_solution, id_experimental_scenario]
        # First retrieve expected solution and experimental scenario objects
        solution_aux = session.query(ExpectedSolution).filter(ExpectedSolution.id == parameters[2]).first()
        exp_scenario_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[3]).first()
        problem_aux = Problem(parameters[0], parameters[1], solution_aux, exp_scenario_aux)
        session.add(problem_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'Problems' registered into the DB. The list contains a string representation of
        each 'Problem' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 0:    # Asks for all problems stored in the database
            problems = session.query(Problem).all()
            for item in problems:
                msg_rspt.information.append(item.__str__())
        else:   # Asks for all problems associated with an specific experimental scenario
            # Received --> [id_exp_scenario]
            problems_list = []
            solutions_list = []
            problems = session.query(Problem).filter(Problem.experimental_scenario_id == parameters[0]).all()
            for item in problems:
                problems_list.append(item.__str__())
                solutions_list.append(item.expected_solution.__str__())
            msg_rspt.information.append(problems_list)
            msg_rspt.information.append(solutions_list)
        session.close()
        return msg_rspt

    '''@staticmethod
    def update(parameters, session):
        # Received --> [id_problem, brief_description, description, id_i_solution, id_experimental_scenario]
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        i_solution_aux = session.query(ExpectedSolution).filter(ExpectedSolution.id == parameters[3]).first()
        exp_scenario_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[4]).first()
        problem_aux.brief_description = parameters[1]
        problem_aux.description = parameters[2]
        problem_aux.expected_solution = i_solution_aux
        problem_aux.experimental_scenario = exp_scenario_aux
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rsp'''

    @staticmethod
    def delete(parameters, session):
        """
        Removes a 'Problem' object from the DB. The 'parameters' contains de id of the 'Problem' object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_problem]
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        solution_aux = session.query(ExpectedSolution).filter(ExpectedSolution.id == problem_aux.expected_solution_id).first()
        # Delete diagram (only file) tht the expected solution may have
        Diagram.delete([solution_aux.diagram_id, 'just remove path'], session)
        session.delete(problem_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of a 'Problem' object from the DB. The 'parameters' contains de id of
        the desired 'Problem'.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_problem]
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(problem_aux.brief_description)
        msg_rspt.information.append(problem_aux.description)
        msg_rspt.information.append(problem_aux.expected_solution_id)
        msg_rspt.information.append(problem_aux.experimental_scenario_id)
        session.close()
        return msg_rspt
