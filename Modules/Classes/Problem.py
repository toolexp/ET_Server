# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Diagram import Diagram
from Modules.Classes.ExperimentalScenario import ExperimentalScenario
from Modules.Classes.ExpectedSolution import ExpectedSolution


class Problem(Base):
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
        self.brief_description = brief_description
        self.description = description
        self.expected_solution = expected_solution
        self.experimental_scenario = experimental_scenario

    def __str__(self):
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.brief_description, self.description, self.expected_solution_id,
                                       self.experimental_scenario_id)

    @staticmethod
    def create(parameters, session):
        # First create the expected solution
        # Received --> [brief_description, description, id_expected_solution, id_experimental_scenario]
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
        problems = session.query(Problem).all()
        msg_rspt = Message(action=2, information=[])
        for problem in problems:
            msg_rspt.information.append(problem.__str__())
        session.close()
        return msg_rspt

    @staticmethod
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
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        # Received --> [id_problem]
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        # Neccesary to remove diagram path
        solution_aux = session.query(ExpectedSolution).filter(ExpectedSolution.id == problem_aux.expected_solution_id).first()
        Diagram.delete([solution_aux.diagram_id, 'just remove path'], session)
        session.delete(problem_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        # Received --> [id_problem]
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(problem_aux.brief_description)
        msg_rspt.information.append(problem_aux.description)
        msg_rspt.information.append(problem_aux.expected_solution_id)
        msg_rspt.information.append(problem_aux.experimental_scenario_id)
        session.close()
        return msg_rspt
