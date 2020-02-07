# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey, and_
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
        if parameters[1] is not None:   # Solution diagram is optional
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[1]).first()
        else:
            diagram_aux = None
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
    def select(parameters, session):
        from Modules.Classes.ExperimentalScenario import ExperimentalScenario
        from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
        from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
        from Modules.Classes.Problem import Problem
        # Received --> [id_designer, id_problem]
        # Return --> [s_solution_aux.annotations, s_solution_aux.diagram_id, [s_solution_aux.patterns__str__()],
        # designer_group, [patterns_assigned_designer]]
        s_solution_aux = session.query(SentSolution).filter(and_(SentSolution.designer_id == parameters[0],
                                                                 SentSolution.problem_id == parameters[1])).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(s_solution_aux.annotations)
        msg_rspt.information.append(s_solution_aux.diagram_id)
        msg_rspt.information.append([])
        for item in s_solution_aux.patterns:
            msg_rspt.information[2].append(item.__str__())
        # Look for patterns assigned for designer in experimental scenario
        exp_scenario = session.query(ExperimentalScenario).join(ExperimentalScenario.problems).\
            filter(Problem.id == parameters[1]).first()
        type_designer_scenario = session.query(DesignerExperimentalScenario).\
            filter(and_(DesignerExperimentalScenario.experimental_scenario_id == exp_scenario.id,
                        DesignerExperimentalScenario.designer_id == parameters[0])).first()
        msg_rspt.information.append(type_designer_scenario.designer_type)
        type_scenario_patterns = session.query(ExperimentalScenarioPattern).\
            filter(and_(ExperimentalScenarioPattern.experimental_scenario_id == exp_scenario.id,
                        ExperimentalScenarioPattern.pattern_type == type_designer_scenario.designer_type)).all()
        msg_rspt.information.append([])
        for item in type_scenario_patterns:
            msg_rspt.information[4].append(item.pattern_id)
        session.close()
        return msg_rspt
