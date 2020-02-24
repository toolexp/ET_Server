from sqlalchemy import Column, String, Integer, ForeignKey, and_, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.Experiment import Experiment
from Modules.Classes.Diagram import Diagram
from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
from Modules.Classes.Pattern import Pattern
from datetime import datetime


class ExperimentalScenario(Base):
    """
    A class used to represent an experimental scenario. An experimental scenario object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param title: title of the scenario
    :type title: str
    :param description: description given to the scenario
    :type description: str
    :param access_code: unique code used to control access to the scenario
    :type access_code: str
    :param state: current state of the scenario. It may be: created, execution or finished
    :type state: str
    :param availability: indicates whether the scenario is available or not for configured designers
    :type availability: bool
    :param creation_date: datetime when the experiment was created
    :type creation_date: datetime
    :param execution_date: datetime when the experiment was executed (made it available for designers)
    :type execution_date: datetime
    :param finished_date: datetime when the experiment was finished (manually or automatically)
    :type finished_date: datetime
    :param description_diagram_id: identifier of the diagram object that is used to describe the scenario.
    This is a foreign key
    :type description_diagram_id: int
    :param experiment_id: identifier of the experiment object which the scenario belongs to. This is a foreign key
    :type experiment_id: int
    :param description_diagram: diagram object that is used to describe the scenario
    :type description_diagram: Modules.Classes.Diagram.Diagram
    :param experiment: experiment object which the scenario belongs to
    :type experiment: Modules.Classes.Experiment.Experiment
    """

    __tablename__ = 'experimental_scenarios'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    access_code = Column(String)
    state = Column(String)  # created, execution, finished
    availability = Column(Boolean)
    creation_date = Column(DateTime)
    execution_date = Column(DateTime)
    finished_date = Column(DateTime)
    description_diagram_id = Column(Integer, ForeignKey('diagrams.id'))
    experiment_id = Column(Integer, ForeignKey('experiments.id'))

    description_diagram = relationship("Diagram", backref="experimental_scenario", cascade="all, delete-orphan",
                                       single_parent=True, uselist=False)
    experiment = relationship("Experiment", backref=backref("experimental_scenarios", cascade="all, delete-orphan",
                                                            single_parent=True))

    def __init__(self, title, description, access_code, state, description_diagram, experiment):
        """
        Constructor of the class
        """
        self.title = title
        self.description = description
        self.access_code = access_code
        self.state = state
        self.availability = True
        self.description_diagram = description_diagram
        self.experiment = experiment
        self.creation_date = datetime.now()
        self.execution_date = None
        self.finished_date = None

    def __str__(self):
        """
        Method that represents the object as a string
        """
        if self.availability:
            aux_av = '✓'
        else:
            aux_av = ''
        return '{}¥{}¥{}¥{}¥{}'.format(self.id, self.title, self.description, self.state, aux_av)

    @staticmethod
    def create(parameters, session):
        """
        Creates an 'ExperimentalScenario' object and stores it into the DB, the data for the object is inside the
        'parameters' variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        from Modules.Classes.Designer import Designer
        from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
        # Received --> [title, description, access_code, state, description_diagram_id, experiment_id,
        # [experimental_designers_ids...], [control_designers_ids...], [experimental_patterns_ids...],
        # [control_patterns_ids...]]
        experiment = session.query(Experiment).filter(Experiment.id == parameters[5]).first()
        if parameters[4] is not None:   # Description diagram is optional
            description_diagram = session.query(Diagram).filter(Diagram.id == parameters[4]).first()
        else:
            description_diagram = None
        exp_sc_aux = ExperimentalScenario(parameters[0], parameters[1], parameters[2], parameters[3],
                                          description_diagram, experiment)
        session.add(exp_sc_aux)
        # Creation of designers group(s)
        for item in parameters[6]:  # Experimental group always exists
            designer_aux = session.query(Designer).filter(Designer.id == item).first()
            designer_exp_aux = DesignerExperimentalScenario(1, designer_aux, exp_sc_aux)
            session.add(designer_exp_aux)
        if experiment.design_type == 2:  # Experimental design (defined in experiment)
            for item in parameters[7]:  # Control group may exist
                designer_aux = session.query(Designer).filter(Designer.id == item).first()
                designer_exp_aux = DesignerExperimentalScenario(2, designer_aux, exp_sc_aux)
                session.add(designer_exp_aux)
        new_exp_sc_aux = session.query(ExperimentalScenario).order_by(ExperimentalScenario.id.desc()).first()
        # Creation of patterns for designers group(s)
        for item in parameters[8]:  # Patterns for experimental group always exists
            pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
            exp_sc_pat = ExperimentalScenarioPattern(1, new_exp_sc_aux, pattern_aux)
            session.add(exp_sc_pat)
        if experiment.design_type == 2:  # Experimental design (defined in experiment)
            for item in parameters[9]:  # Patterns for control group may exist
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                exp_sc_pat = ExperimentalScenarioPattern(2, new_exp_sc_aux, pattern_aux)
                session.add(exp_sc_pat)
        if parameters[3] == 'execution':    # When an scenario is created with 'execution' state, the experiment
            # containing it has to be in 'execution' as well
            experiment.state = 'execution'
            experiment.execution_date = datetime.now()
        session.commit()
        new_exp_sc_aux = session.query(ExperimentalScenario).order_by(ExperimentalScenario.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[new_exp_sc_aux.id], comment='Register created successfully')
        return msg_rspt

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'ExperimentalScenarios' registered into the DB. The list contains a string representation of
        each 'ExperimentalScenario' (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        if len(parameters) == 0:    # Ask for all experimental scenarios registered in the DB
            exp_scenarios = session.query(ExperimentalScenario).all()
        elif len(parameters) == 1:  # Ask for all experimental scenarios associated with an experiment
            # Received --> [id_experiment]
            exp_scenarios = session.query(ExperimentalScenario).filter(
                ExperimentalScenario.experiment_id == parameters[0]).all()
        else:   # When a designer retrieves available scenarios for him
            from Modules.Classes.Measurement import Measurement
            from Modules.Classes.Designer import Designer
            from Modules.Classes.Problem import Problem
            from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
            # Received --> ['my scenarios', id_designer]
            exp_scenarios = session.query(ExperimentalScenario). \
                join(ExperimentalScenario.designer_associations). \
                join(DesignerExperimentalScenario.designer).filter(and_(Designer.id == parameters[1],
                                                                        ExperimentalScenario.state == 'execution',
                                                                        ExperimentalScenario.availability == True)).all()
            exp_scenarios_done = session.query(ExperimentalScenario). \
                join(ExperimentalScenario.problems). \
                join(Problem.measurements).filter(Measurement.designer_id == parameters[1]).all()
            for item in exp_scenarios_done:
                if item in exp_scenarios:   # Exclude scenarios that have been aready completed
                    exp_scenarios.remove(item)
        msg_rspt = Message(action=2, information=[])
        for item in exp_scenarios:
            msg_rspt.information.append(item.__str__())
        session.close()
        return msg_rspt

    @staticmethod
    def update(parameters, session):
        """
        Updates an 'ExperimentalScenario' object from the DB, the id and new data for the object is inside the
        'parameters' variable.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        if len(parameters) == 3:    # To cahnge availability of scenario for designers
            # Received --> ['change_availability', id_exp_sc, new_state]
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[1]).first()
            exp_sc_aux.availability = parameters[2]
        elif len(parameters) == 2:  # Finish an experimental scenario when all designers executed it
            from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
            from Modules.Classes.Measurement import Measurement
            # Received --> ['finished', id_exp_sc]
            change_state = True
            designers_exp_sc = session.query(DesignerExperimentalScenario).\
                filter(DesignerExperimentalScenario.experimental_scenario_id == parameters[1]).all()
            for item in designers_exp_sc:   # Check if there exists measurements for all designers in selected
                # experimental scenarios
                measurements_aux = session.query(Measurement).filter(Measurement.designer_id == item.designer_id).all()
                if measurements_aux:
                    num_measurements = 0
                    for item2 in measurements_aux:
                        if item2.problem.experimental_scenario_id == parameters[1]:
                            break
                        num_measurements += 1
                    if num_measurements == len(measurements_aux):
                        change_state = False
                        break
                else:
                    change_state = False
                    break
            if change_state:
                exp_sc_aux = session.query(ExperimentalScenario).filter(
                    ExperimentalScenario.id == parameters[1]).first()
                exp_sc_aux.state = parameters[0]
                exp_sc_aux.finished_date = datetime.now()
        else:   # Ask for updating the main information of an experimental scenario
            from Modules.Classes.Designer import Designer
            from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
            # Received --> [id_exp_sc, title, description, access_code, description_diagram_id, experiment_id,
            # [control_designers_ids...], [experimental_designers_ids...], [experimental_patterns_ids...],
            # [control_patterns_ids...]]
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
            experiment = session.query(Experiment).filter(Experiment.id == parameters[5]).first()
            if parameters[4] is not None:  # Description diagram is optional
                description_diagram = session.query(Diagram).filter(Diagram.id == parameters[4]).first()
            else:
                description_diagram = None
            exp_sc_aux.title = parameters[1]
            exp_sc_aux.description = parameters[2]
            exp_sc_aux.access_code = parameters[3]
            exp_sc_aux.description_diagram = description_diagram
            exp_sc_aux.experiment = experiment
            # Removing current associated designers
            designers_exp_aux = session.query(DesignerExperimentalScenario).\
                filter(DesignerExperimentalScenario.experimental_scenario_id == parameters[0]).all()
            for item in designers_exp_aux:
                session.delete(item)
            # Creation of designers group(s)
            for item in parameters[6]:  # Control group always exists
                designer_aux = session.query(Designer).filter(Designer.id == item).first()
                designer_exp_aux = DesignerExperimentalScenario(1, designer_aux, exp_sc_aux)
                session.add(designer_exp_aux)
            if experiment.design_type == 2:  # Experimental design (defined in experiment)
                for item in parameters[7]:  # Experimental group may exist
                    designer_aux = session.query(Designer).filter(Designer.id == item).first()
                    designer_exp_aux = DesignerExperimentalScenario(2, designer_aux, exp_sc_aux)
                    session.add(designer_exp_aux)
            # Removing current associated patterns
            patterns_exp_aux = session.query(ExperimentalScenarioPattern). \
                filter(ExperimentalScenarioPattern.experimental_scenario_id == parameters[0]).all()
            for item in patterns_exp_aux:
                session.delete(item)
            # Creation of patterns for each designers group
            for item in parameters[8]:  # Control group always exists
                pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                patterns_exp_aux = ExperimentalScenarioPattern(1, exp_sc_aux, pattern_aux)
                session.add(patterns_exp_aux)
            if experiment.design_type == 2:  # Experimental design (defined in experiment)
                for item in parameters[9]:  # Experimental group may exist
                    pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
                    patterns_exp_aux = ExperimentalScenarioPattern(2, exp_sc_aux, pattern_aux)
                    session.add(patterns_exp_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes an 'ExperimentalScenario' object from the DB. The 'parameters' contains de id of the
        'ExperimentalScenario' object.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_exp_scenario]
        exp_scenario_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
        # Neccesary to remove diagrams files if existing from files storage
        if exp_scenario_aux.description_diagram is not None:
            Diagram.delete([exp_scenario_aux.description_diagram_id, 'just remove path'], session)
        for item in exp_scenario_aux.problems:
            if item.expected_solution.diagram_id is not None:
                Diagram.delete([item.expected_solution.diagram_id, 'just remove path'], session)
        session.delete(exp_scenario_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt

    @staticmethod
    def select(parameters, session):
        """
        Retrieve information (attributes) of an 'ExperimentalScenario' object from the DB. The 'parameters' contains de
        id of the desired 'ExperimentalScenario'.

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 2:    # Get role of designer for current experimental scenario (control or experimental)
            from Modules.Classes.Designer import Designer
            from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
            # Received --> [id_designer, id_exp_scenario]
            exp_scenario = session.query(DesignerExperimentalScenario). \
                filter(and_(DesignerExperimentalScenario.designer_id == parameters[0],
                            DesignerExperimentalScenario.experimental_scenario_id == parameters[1])).first()
            if exp_scenario.designer_type == 1:
                msg_rspt.information.append('experimental')
            else:
                msg_rspt.information.append('control')
        elif len(parameters) == 1:  # Ask for information of an specific experimental scenario
            # Received --> [id_exp_scenario]
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
            msg_rspt.information.append(exp_sc_aux.title)
            msg_rspt.information.append(exp_sc_aux.description)
            msg_rspt.information.append(exp_sc_aux.access_code)
            msg_rspt.information.append(exp_sc_aux.state)
            msg_rspt.information.append(exp_sc_aux.availability)
            msg_rspt.information.append(exp_sc_aux.description_diagram_id)
            msg_rspt.information.append(exp_sc_aux.experiment_id)
        else:   # Ask for information of an scenario to be shown as summary of the report
            from Modules.Classes.Designer import Designer
            from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
            from Modules.Classes.Measurement import Measurement
            from Modules.Classes.Problem import Problem
            # Received --> [id_exp_scenario, 'report', aux]
            exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
            msg_rspt.information.append(exp_sc_aux.title)
            msg_rspt.information.append(exp_sc_aux.description)
            msg_rspt.information.append(exp_sc_aux.description_diagram_id)
            msg_rspt.information.append([])
            for item in exp_sc_aux.problems:
                msg_rspt.information[3].append(item.__str__())
            # Retrieve main information of designers associated with the scenario
            problems = session.query(Problem). \
                join(Problem.experimental_scenario). \
                filter(ExperimentalScenario.id == parameters[0]).all()
            all_designers = session.query(Designer). \
                join(Designer.experimental_scenario_associations). \
                join(DesignerExperimentalScenario.experimental_scenario).\
                filter(ExperimentalScenario.id == parameters[0]).all()
            done_designers = session.query(Designer). \
                join(Designer.measurements). \
                join(Measurement.problem).join(Problem.experimental_scenario). \
                filter(and_(ExperimentalScenario.id == parameters[0], Measurement.value >= 0)).all()
            # There is the possibility that a designer exited the scenario while it was in execution (maybe completed
            # one of two problems) the above query will show that the designer completed both problems, when not
            aux_done_designers = done_designers
            for item in problems:
                # Check for each problem of the scenario if have been completed succesfullly
                done_designers_problem = session.query(Designer). \
                    join(Designer.measurements). \
                    join(Measurement.problem). \
                    filter(and_(Problem.id == item.id, Measurement.value >= 0)).all()
                # If at least one problem not completed, the the whole scenario was not completed
                if len(done_designers) != len(done_designers_problem):
                    aux_done_designers = done_designers if len(done_designers) < len(done_designers_problem) else done_designers_problem
            done_designers = aux_done_designers
            exit_designers = session.query(Designer). \
                join(Designer.measurements). \
                join(Measurement.problem).join(Problem.experimental_scenario). \
                filter(and_(ExperimentalScenario.id == parameters[0], Measurement.value == -2)).all()
            not_done_designers = session.query(Designer). \
                join(Designer.measurements). \
                join(Measurement.problem).join(Problem.experimental_scenario). \
                filter(and_(ExperimentalScenario.id == parameters[0], Measurement.value == -1)).all()
            number_designers = [len(all_designers), len(done_designers), len(exit_designers), len(not_done_designers)]
            msg_rspt.information.append(number_designers)
        session.close()
        return msg_rspt
