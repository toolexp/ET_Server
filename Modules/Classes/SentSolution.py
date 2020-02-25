from sqlalchemy import Column, String, Integer, Table, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Diagram import Diagram


sent_solutions_patterns_association = Table(
    """
    Many to many association table generated into the DB
    """
    'sent_solutions_patterns', Base.metadata,
    Column('sent_solution_id', Integer, ForeignKey('sent_solutions.id')),
    Column('pattern_id', Integer, ForeignKey('patterns.id'))
)


class SentSolution(Base):
    """
    A class used to represent a sent solution to a design problem given by a designer. A sent solution object has
    attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param annotations: annotations included in the sent solution
    :type annotations: str
    :param diagram_id: identifier of the diagram object that the sent solution may have. This is a foreign key
    :type diagram_id: int
    :param designer_id: identifier of the designer object of whom the sent solution is. This is a foreign key
    :type designer_id: int
    :param problem_id: identifier of the problem object that the sent solution is associated to. This is a foreign key
    :type problem_id: int
    :param diagram: diagram object that the sent solution may have
    :type diagram: Modules.Classes.Diagram.Diagram
    :param designer: designer object of whom the sent solution is
    :type designer: Modules.Classes.Designer.Designer
    :param problem: problem object that the sent solution is associated to
    :type problem: Modules.Classes.Problem.Problem
    :param patterns: list of pattern objects that the sent solution may have
    :type patterns: list[Modules.Classes.Pattern.Pattern]
    """
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
        """
        Constructor of the class
        """
        self.annotations = annotations
        self.diagram = diagram
        self.designer = designer
        self.problem = problem

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}'.format(self.id, self.annotations)

    @staticmethod
    def create(parameters, session):
        """
        Creates a 'SentSolution' object and stores it into the DB, the data for the object is inside the
        'parameters' variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
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
            # With patterns--> parameters=[annotations, id_diagram, id_designer, id_problem,
            # [id_pattern1, id_pattern2, ...]]
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
        """
        Retrieve information (attributes) of an 'SentSolution' object from the DB. The 'parameters' contains de
        id of the desired 'SentSolution'. Each attribute occupies a space of the returned list.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.ExperimentalScenario import ExperimentalScenario
        from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
        from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
        from Modules.Classes.Problem import Problem
        # Received --> [id_designer, id_problem]
        s_solution_aux = session.query(SentSolution).filter(and_(SentSolution.designer_id == parameters[0],
                                                                 SentSolution.problem_id == parameters[1])).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(s_solution_aux.annotations)
        msg_rspt.information.append(s_solution_aux.diagram_id)
        msg_rspt.information.append([])
        for item in s_solution_aux.patterns:    # Append sent solution patterns
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
        for item in type_scenario_patterns:     # Append designer's assigned patterns in problem
            msg_rspt.information[4].append(item.pattern_id)
        session.close()
        # Return --> [s_solution_aux.annotations, s_solution_aux.diagram_id, [s_solution_aux.patterns__str__()],
        # designer_group, [patterns_assigned_designer]]
        return msg_rspt
