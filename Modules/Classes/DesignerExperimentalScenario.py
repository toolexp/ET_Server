from sqlalchemy import Column, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from Modules.Config.base import Base
from Modules.Config.Data import Message
from Modules.Classes.ExperimentalScenario import ExperimentalScenario


class DesignerExperimentalScenario(Base):
    """
    A class used to represent an association object between a designer and an experimental scenario.
    An association object has attributes:

    :param id: identifier of object in the database. This is the primary key
    :type id: int
    :param designer_type: indicator of a designer's membership type to a group in a scenario (experimental or control)
    :type designer_type: int
    :param designer_id: identifier of the designer object that belongs to the association. This is a foreign key
    :type designer_id: int
    :param experimental_scenario_id: identifier of the experimental_scenario object that belongs to the association.
    This is a foreign key
    :type experimental_scenario_id: int
    :param designer: designer object that belongs to the association
    :type designer: Module.Classes.Designer.Designer
    :param experimental_scenario: experimental scenario object that belongs to the association
    :type experimental_scenario: Module.Classes.ExperimentalScenario.ExperimentalScenario
    """

    __tablename__ = 'designer_experimental_scenarios'

    id = Column(Integer, primary_key=True)
    designer_type = Column(Integer)   # Indicates whether the designer belongs to the control group or experimental
    # group in an specific experimental scenario
    designer_id = Column(Integer, ForeignKey('designers.id'))
    experimental_scenario_id = Column(Integer, ForeignKey('experimental_scenarios.id'))

    designer = relationship("Designer",
                            backref=backref("experimental_scenario_associations", cascade="all, delete-orphan"))
    experimental_scenario = relationship("ExperimentalScenario",
                                         backref=backref("designer_associations", cascade="all, delete-orphan"))

    def __init__(self, designer_type, designer, experimental_scenario):
        """
        Constructor of the class
        """
        self.designer_type = designer_type    # if designer_type=1 --> experimental group, otherwise control group
        self.designer = designer
        self.experimental_scenario = experimental_scenario

    def __str__(self):
        """
        Method that represents the object as a string
        """
        return '{}¥{}¥{}¥{}'.format(self.id, self.designer_type, self.designer_id, self.experimental_scenario_id)

    @staticmethod
    def read(parameters, session):
        """
        Retrieves a list of 'DesignerExperimentalScenario' registered into the DB. The target objects depends of the
        length of the 'parameters'. The list contains a string representation of each 'DesignerExperimentalScenario'
        (__str__()).

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        msg_rspt = Message(action=2, information=[])
        if len(parameters) == 0:    # Ask for all associations stored in DB
            des_exp_scenarios = session.query(DesignerExperimentalScenario).all()
            for item in des_exp_scenarios:
                msg_rspt.information.append(item.__str__())
        else:   # Ask for designers of an experimental scenario, separated by groups
            # Received --> [id_exp_scenario]
            from Modules.Classes.Designer import Designer
            # Get all associations of the queried scenario
            des_exp_scenarios = session.query(DesignerExperimentalScenario).filter(
                DesignerExperimentalScenario.experimental_scenario_id == parameters[0]).all()
            exp_designers = []
            ctrl_designers = []
            for item in des_exp_scenarios:
                # Get designer from current association object
                designer_aux = session.query(Designer).filter(Designer.id == item.designer_id).first()
                if item.designer_type == 1:   # if designer_type=1 --> experimental group, otherwise control group
                    exp_designers.append(designer_aux.__str__())
                else:
                    ctrl_designers.append(designer_aux.__str__())
            msg_rspt.information.append(exp_designers)
            msg_rspt.information.append(ctrl_designers)
        session.close()
        return msg_rspt

    @staticmethod
    def delete(parameters, session):
        """
        Removes all 'DesignerExperimentalScenario' object from the DB which design type is 'experimental'. The
        'parameters' contains de id of the 'Experiment' object that contains all experimental scenarios from which
        the target 'DesignerExperimentalScenario' objects are. This function is called only when an experiment is
        updated from 'experimental' to 'control' design type

        :param parameters: list of important information that is needed in this function
        :type parameters: list
        :param session: session established with the database
        :type session: Modules.Config.base.Session
        :return msg_rspt: message ready to send to a client (response of requested action)
        :rtype msg_rspt: Modules.Config.Data.Message
        """
        # Received --> [id_exeriment]
        # Retrieve all scenarios associated with target experiment
        exp_sc = session.query(ExperimentalScenario).filter(ExperimentalScenario.experiment_id == parameters[0]).all()
        for item in exp_sc:
            # Retrieve all DesignerExperimentalScenario association for current experimental scenario
            exp_scenarios_pat = session.query(DesignerExperimentalScenario).filter(and_(
                DesignerExperimentalScenario.experimental_scenario_id == item.id,
                DesignerExperimentalScenario.designer_type == 2)).all()
            for item2 in exp_scenarios_pat:
                session.delete(item2)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt