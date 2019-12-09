# coding=utf-8

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Diagram import Diagram


ideal_solutions_patterns_association = Table(
    'ideal_solutions_patterns', Base.metadata,
    Column('ideal_solution_id', Integer, ForeignKey('ideal_solutions.id')),
    Column('pattern_id', Integer, ForeignKey('patterns.id'))
)


class IdealSolution(Base):
    __tablename__ = 'ideal_solutions'

    id = Column(Integer, primary_key=True)
    annotations = Column(String)
    diagram_id = Column(Integer, ForeignKey('diagrams.id'))

    diagram = relationship("Diagram", backref="ideal_solution", cascade="all, delete-orphan", single_parent=True, uselist=False)

    # Relation many to many
    patterns = relationship("Pattern", secondary=ideal_solutions_patterns_association, backref='ideal_solutions')

    def __init__(self, annotations, diagram):
        self.annotations = annotations
        self.diagram = diagram

    def __str__(self):
        return '{}¥{}¥{}'.format(self.id, self.annotations, self.diagram_id)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.Pattern import Pattern
        if len(parameters) == 2:
            # Wthout patterns --> parameters=[annotations, id_diagram]
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[1]).first()
            i_solution_aux = IdealSolution(parameters[0], diagram_aux)
        else:
            # With patterns--> parameters=[annotations, id_diagram, [id_pattern1, id_pattern2, ...]]
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[1]).first()
            i_solution_aux = IdealSolution(parameters[0], diagram_aux)
            i_solution_aux.patterns = []
            for item in parameters[2]:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                i_solution_aux.patterns.append(pattern_aux)
        session.add(i_solution_aux)
        session.commit()
        new_i_sol_aux = session.query(IdealSolution).order_by(IdealSolution.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[new_i_sol_aux.id], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        from Modules.Classes.Pattern import Pattern
        i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
        i_solution_aux.annotations = parameters[1]
        i_solution_aux.diagram = diagram_aux
        i_solution_aux.patterns = []
        if len(parameters) == 4:
            # With patterns--> parameters=[id_i_solution, annotations, id_diagram, [id_pattern1, id_pattern2, ...]]
            for item in parameters[3]:
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                i_solution_aux.patterns.append(pattern_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
        session.delete(i_solution_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(i_solution_aux.annotations)
        msg_rspt.information.append(i_solution_aux.diagram_id)
        msg_rspt.information.append([])
        for i in range(0, len(i_solution_aux.patterns)):
            msg_rspt.information[2].append(i_solution_aux.patterns[i].__str__())
        session.close()
        return msg_rspt
