# coding=utf-8

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Category import Category
from Modules.Classes.Pattern import Pattern
from Modules.Classes.Problem import Problem
from Modules.Classes.ScenarioComponentPattern import ScenarioComponentPattern


class ScenarioComponent(Base):
    __tablename__ = 'scenario_components'

    id = Column(Integer, primary_key=True)
    experimental_scenario_id = Column(Integer, ForeignKey('experimental_scenarios.id'))
    problem_id = Column(Integer, ForeignKey('problems.id'))

    experimental_scenario = relationship("ExperimentalScenario", backref=backref("scenario_components",
                                                                                 cascade="all, delete-orphan",
                                                                                 single_parent=True))
    problem = relationship("Problem", backref=backref("scenario_components", cascade="all, delete-orphan",
                                                      single_parent=True))
    #patterns = relationship("Pattern", secondary="scenario_components_patterns", backref="scenario_components")
    patterns = relationship("Pattern", secondary="scenario_components_patterns", viewonly=True)

    def __init__(self, experimental_scenario, problem):
        self.experimental_scenario = experimental_scenario
        self.problem = problem

    def __str__(self):
        return '{}¥{}¥{}'.format(self.id, self.experimental_scenario_id, self.problem_id)

    @staticmethod
    def create(parameters, session):
        from Modules.Classes.ExperimentalScenario import ExperimentalScenario
        # Received --> [experimental_scenario_id, problem_id, [cgroup_pattern_id1, cgroup_pattern_id2, ...], [egroup_pattern_id1, egroup_pattern_id2, ...]]
        experimental_scenario_aux = session.query(ExperimentalScenario).filter(
            ExperimentalScenario.id == parameters[0]).first()
        problem_aux = session.query(Problem).filter(Problem.id == parameters[1]).first()
        sc_component_aux = ScenarioComponent(experimental_scenario_aux, problem_aux)
        session.add(sc_component_aux)
        # Creating association of scenario component and patterns for the control group
        for item in parameters[2]:
            pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
            scc_pattern_aux = ScenarioComponentPattern(1, sc_component_aux, pattern_aux)
            session.add(scc_pattern_aux)
        # Creating association of scenario component and patterns for the experimental group
        for item in parameters[3]:
            pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
            scc_pattern_aux = ScenarioComponentPattern(2, sc_component_aux, pattern_aux)
            session.add(scc_pattern_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        # Received --> []
        if len(parameters) == 0:
            sc_components = session.query(ScenarioComponent).all()
        else:
            # Received --> [id_exp_scenario, 1]
            # Ask for the scenario components associated with an experimental scenario
            if parameters[1] == 1:
                sc_components = session.query(ScenarioComponent).filter(
                    ScenarioComponent.experimental_scenario_id == parameters[0]).all()
            # Received --> [id_sc_component, 2]
            # Ask for the patterns associated with an scenario components
            else:
                sc_components = session.query(ScenarioComponentPattern).filter(
                    ScenarioComponentPattern.scenario_component_id == parameters[0]).all()
        msg_rspt = Message(action=2, information=[])
        for item in sc_components:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        # Received --> [sc_comp_id, problem_id, [cgroup_pattern_id1, cgroup_pattern_id2, ...], [egroup_pattern_id1, egroup_pattern_id2, ...]]
        sc_comp_aux = session.query(ScenarioComponent).filter(ScenarioComponent.id == parameters[0]).first()
        problem_aux = session.query(Problem).filter(Problem.id == parameters[1]).first()
        sc_comp_aux.problem = problem_aux
        # Deleting association of scenario component with pattern
        sc_comp_pat = session.query(ScenarioComponentPattern). \
            filter(ScenarioComponentPattern.scenario_component_id == parameters[0]).all()
        for item in sc_comp_pat:
            session.delete(item)
        # Creating association of scenario component and patterns for the control group
        for item in parameters[2]:
            pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
            scc_pattern_aux = ScenarioComponentPattern(1, sc_comp_aux, pattern_aux)
            session.add(scc_pattern_aux)
        # Creating association of scenario component and patterns for the experimental group
        for item in parameters[3]:
            pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
            scc_pattern_aux = ScenarioComponentPattern(2, sc_comp_aux, pattern_aux)
            session.add(scc_pattern_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        # Received --> [id_sc_component]
        sc_comp_aux = session.query(ScenarioComponent).filter(ScenarioComponent.id == parameters[0]).first()
        session.delete(sc_comp_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        category_aux = session.query(Category).filter(Category.id == parameters[0]).first()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(category_aux.name)
        msg_rspt.information.append(category_aux.classification_id)
        session.close()
        return msg_rspt
