# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Diagram import Diagram


sent_solutions_patterns_association = Table(
    'sent_solutions_patterns', Base.metadata,
    Column('sent_solution_id', Integer, ForeignKey('sent_solutions.id')),
    Column('pattern_id', Integer, ForeignKey('patterns.id'))
)


class SentSolution(Base):
    __tablename__ = 'sent_solutions'

    id = Column(Integer, primary_key=True)
    annotations = Column(String)
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    designer_id = Column(Integer, ForeignKey('designers.id'))
    problem_id = Column(Integer, ForeignKey('problems.id'))

    diagram = relationship("Diagram", backref="sent_solutions", cascade="all, delete-orphan", single_parent=True,
                           uselist=False)
    designer = relationship("Designer", backref=backref("sent_solutions", cascade="all, delete-orphan",
                                                        single_parent=True))
    problem = relationship("Problem", backref=backref("sent_solutions", cascade="all, delete-orphan",
                                                      single_parent=True))
    # Relation many to many
    patterns = relationship("Pattern", secondary=sent_solutions_patterns_association, backref='sent_solutions')

    def __init__(self, annotations, diagram, designer, problem):
        self.annotations = annotations
        self.diagram = diagram
        self.designer = designer
        self.problem = problem

    def __str__(self):
        return '{}¥{}'.format(self.id, self.annotations)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.Designer import Designer
        from Modules.Classes.Pattern import Pattern
        from Modules.Classes.Problem import Problem
        # Wthout patterns --> parameters=[annotations, id_diagram, id_designer, id_problem]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[1]).first()
        designer_aux = session.query(Designer).filter(Designer.id == parameters[2]).first()
        problem_aux = session.query(Problem).filter(Problem.id == parameters[3]).first()
        s_solution_aux = SentSolution(parameters[0], diagram_aux, designer_aux, problem_aux)
        if len(parameters) == 5:
            # With patterns--> parameters=[annotations, id_diagram, id_designer, id_problem, [id_pattern1, id_pattern2, ...]]
            s_solution_aux.patterns = []
            for item in parameters[4]:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                s_solution_aux.patterns.append(pattern_aux)
        session.add(s_solution_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        sent_sols = session.query(SentSolution).all()
        msg_rspt = Message(action=2, information=[])
        for solutions in sent_sols:
            msg_rspt.information.append(solutions.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        from Modules.Classes.Designer import Designer
        from Modules.Classes.Pattern import Pattern
        from Modules.Classes.Problem import Problem
        s_solution_aux = session.query(SentSolution).filter(SentSolution.id == parameters[0]).first()
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
        designer_aux = session.query(Designer).filter(Designer.id == parameters[3]).first()
        problem_aux = session.query(Problem).filter(Problem.id == parameters[4]).first()
        s_solution_aux.annotations = parameters[1]
        s_solution_aux.diagram = diagram_aux
        s_solution_aux.designer = designer_aux
        s_solution_aux.problem = problem_aux
        s_solution_aux.patterns = []
        if len(parameters) == 6:
            # With patterns--> parameters=[id_s_solution, annotations, id_diagram, id_designer, id_problem,
            # [id_pattern1, id_pattern2, ...]]
            for item in parameters[5]:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                s_solution_aux.patterns.append(pattern_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        s_solution_aux = session.query(SentSolution).filter(SentSolution.id == parameters[0]).first()
        session.delete(s_solution_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        s_solution_aux = session.query(SentSolution).filter(SentSolution.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(s_solution_aux.annotations)
        msg_rspt.information.append(s_solution_aux.diagram_id)
        msg_rspt.information.append(s_solution_aux.designer_id)
        msg_rspt.information.append(s_solution_aux.problem_id)
        msg_rspt.information.append([])
        for i in range(0, len(s_solution_aux.patterns)):
            msg_rspt.information[2].append(s_solution_aux.patterns[i].__str__())
        session.close()
        return msg_rspt
