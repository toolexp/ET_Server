# coding=utf-8

# Import necessary modules
from datetime import date
from Modules.Config.base import Session, engine, Base

from Modules.Classes.Administrator import Administrator
from Modules.Classes.Section import Attribute
from Modules.Classes.Designer import Designer
from Modules.Classes.DesignersGroup import DesignersGroup
from Modules.Classes.Diagram import Diagram
from Modules.Classes.Experiment import Experiment
from Modules.Classes.ExperimentalScenario import ExperimentalScenario
from Modules.Classes.Experimenter import Experimenter
from Modules.Classes.IdealSolution import IdealSolution
from Modules.Classes.Pattern import Pattern
from Modules.Classes.PatternSection import PatternSection
from Modules.Classes.Problem import Problem
from Modules.Classes.ScenarioComponent import ScenarioComponent
from Modules.Classes.ScenarioComponentPattern import ScenarioComponentPattern
from Modules.Classes.SentSolution import SentSolution
from Modules.Classes.Template import Template

# Create session with DB
Base.metadata.create_all(engine)
session = Session()

# Get data from DB
#admin_demo = session.query(Administrator).filter(Administrator.name == 'demo_name').first()
#designer_demo = session.query(Designer).filter(Designer.name == 'demo_name').first()
#designers_group_demo = session.query(DesignersGroup).filter(DesignersGroup.name == 'demo_name').first()
#experimenter_demo = session.query(Experimenter).filter(Experimenter.name == 'demo_name').first()
#experiment_demo = session.query(Experiment).filter(Experimenter.name == 'demo_name').first()
#attribute_demo = session.query(Attribute).filter(Attribute.name == 'demo_name').first()
#sent_sol_demo = session.query(SentSolution).filter(SentSolution.name == 'demo_name').first()
diagrama_demo = session.query(Diagram).filter(Diagram.name == 'demo_name').first()


# Delete data
'''
session.delete(admin_demo)
session.delete(designer_demo)
session.delete(experimenter_demo)
session.delete(attribute_demo)
session.delete(sent_sol_demo)
'''
session.delete(diagrama_demo)

# Save changes and close connection
session.commit()
session.close()