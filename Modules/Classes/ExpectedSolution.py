from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Diagram import Diagram


expected_solutions_patterns_association = Table(
    """
    Many to many association table generated into the DB
    """
    'expected_solutions_patterns', Base.metadata,
    Column('expected_solution_id', Integer, ForeignKey('expected_solutions.id')),
    Column('pattern_id', Integer, ForeignKey('patterns.id'))
)


class ExpectedSolution(Base):
    """
    A class used to represent an expected solution to a design problem. An expected solution object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param annotations: annotations included in the expected solution
    :type annotations: str
    :param diagram_id: identifier of the diagram object that the expected solution may have. This is a foreign key
    :type diagram_id: int
    :param diagram: diagram object that the expected solution may have
    :type diagram: Modules.Classes.Diagram.Diagram
    :param patterns: list of pattern objects that the expected solution may have
    :type patterns: list[Modules.Classes.Pattern.Pattern]
    """

    __tablename__ = 'expected_solutions'

    id = Column(Integer, primary_key=True)
    annotations = Column(String)
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))

    diagram = relationship("Diagram", backref="expected_solution", cascade="all, delete-orphan", single_parent=True,
                           uselist=False)

    # Relation many to many
    patterns = relationship("Pattern", secondary=expected_solutions_patterns_association, backref='expected_solutions')

    def __init__(self, annotations, diagram):
        """
        Constructor of the class
        """
        self.annotations = annotations
        self.diagram = diagram

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}'.format(self.id, self.annotations, self.diagram_id)

    @staticmethod
    def create(parameters, session):
        """
        Creates an 'ExpectedSolution' object and stores it into the DB, the data for the object is inside the
        'parameters' variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.Pattern import Pattern
        if parameters[1] is not None:   # If a diagram has been created for the expected solution
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[1]).first()
        else:   # If no diagram configured
            diagram_aux = None
        if len(parameters) == 2:
            # Wthout patterns --> parameters=[annotations, id_diagram]
            e_solution_aux = ExpectedSolution(parameters[0], diagram_aux)
        else:
            # With patterns--> parameters=[annotations, id_diagram, [id_pattern1, id_pattern2, ...]]
            e_solution_aux = ExpectedSolution(parameters[0], diagram_aux)
            e_solution_aux.patterns = []
            for item in parameters[2]:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                e_solution_aux.patterns.append(pattern_aux)
        session.add(e_solution_aux)
        session.commit()
        new_e_sol_aux = session.query(ExpectedSolution).order_by(ExpectedSolution.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[new_e_sol_aux.id], comment='Register created successfully')
        return msg_rspt

    '''@staticmethod
    def update(parameters, session):
        from Modules.Classes.Pattern import Pattern
        e_solution_aux = session.query(ExpectedSolution).filter(ExpectedSolution.id == parameters[0]).first()
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
        e_solution_aux.annotations = parameters[1]
        e_solution_aux.diagram = diagram_aux
        e_solution_aux.patterns = []
        if len(parameters) == 4:
            # With patterns--> parameters=[id_e_solution, annotations, id_diagram, [id_pattern1, id_pattern2, ...]]
            for item in parameters[3]:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                e_solution_aux.patterns.append(pattern_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        e_solution_aux = session.query(ExpectedSolution).filter(ExpectedSolution.id == parameters[0]).first()
        session.delete(e_solution_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=  2, comment='Register deleted successfully')
        return msg_rspt'''

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of an 'ExpectedSolution' object from the DB. The 'parameters' contains de
        id of the desired 'ExpectedSolution'. Each attribute occupies a space of the returned list.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        e_solution_aux = session.query(ExpectedSolution).filter(ExpectedSolution.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(e_solution_aux.annotations)
        msg_rspt.information.append(e_solution_aux.diagram_id)
        msg_rspt.information.append([])
        for item in e_solution_aux.patterns:
            msg_rspt.information[2].append(item.__str__())
        session.close()
        return msg_rspt
