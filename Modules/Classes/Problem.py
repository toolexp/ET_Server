# coding=utf-8

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Diagram import Diagram
from Modules.Classes.IdealSolution import IdealSolution


class Problem(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    ideal_solution_id = Column(Integer, ForeignKey('ideal_solutions.id'))

    #ideal_solution = relationship("IdealSolution", backref=backref("problems", cascade="all, delete-orphan",
                                                                   #single_parent=True))

    #ideal_solution = relationship("IdealSolution", foreign_keys=ideal_solution_id, post_update=True, cascade="all, delete-orphan",
                                  #single_parent=True)
    ideal_solution = relationship("IdealSolution", backref="problem", cascade="all, delete-orphan", single_parent=True,
                                  uselist=False)

    def __init__(self, name, description, ideal_solution):
        self.name = name
        self.description = description
        self.ideal_solution = ideal_solution

    def __str__(self):
        return '{}¥{}¥{}¥{}'.format(self.id, self.name, self.description, self.ideal_solution_id)

    @staticmethod
    def create(parameters, session):
        # First create the ideal solution
        # Received --> [name, description, id_i_solution]
        solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[2]).first()
        problem_aux = Problem(parameters[0], parameters[1], solution_aux)
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
        # Received --> [id_problem, name, description, id_i_solution]
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[3]).first()
        problem_aux.name = parameters[1]
        problem_aux.description = parameters[2]
        problem_aux.ideal_solution = i_solution_aux
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        from Modules.Classes.ScenarioComponent import ScenarioComponent
        # Received --> [id_problem]
        scenario_comp_aux = session.query(ScenarioComponent).filter(ScenarioComponent.problem_id == parameters[0]).first()
        if scenario_comp_aux:
            return Message(action=5, information=['The problem is associated to one or more experimental scenarios'],
                           comment='Error deleting register')
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        # Neccesary to remove diagram path
        solution_aux = session.query(IdealSolution).filter(IdealSolution.id == problem_aux.ideal_solution_id).first()
        Diagram.delete([solution_aux.diagram_id, 'just remove path'], session)
        session.delete(problem_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        # Received --> [id_problem]
        if len(parameters) == 2:
            from Modules.Classes.ScenarioComponent import ScenarioComponent
            scenario_comp_aux = session.query(ScenarioComponent).filter(
                ScenarioComponent.problem_id == parameters[0]).first()
            if scenario_comp_aux:
                return Message(action=5, information=['The problem is associated to one or more experimental scenarios'],
                               comment='Error selecting register')
        problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(problem_aux.name)
        msg_rspt.information.append(problem_aux.description)
        msg_rspt.information.append(problem_aux.ideal_solution_id)
        session.close()
        return msg_rspt
