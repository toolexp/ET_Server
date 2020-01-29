# coding=utf-8

# Import necessary modules
import hashlib
from datetime import datetime

from Modules.Config.base import Session, engine, Base
from Modules.Classes.Administrator import Administrator
from Modules.Classes.Category import Category
from Modules.Classes.Classification import Classification
from Modules.Classes.Designer import Designer
from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
from Modules.Classes.Diagram import Diagram
from Modules.Classes.Experiment import Experiment
from Modules.Classes.ExperimentalScenario import ExperimentalScenario
from Modules.Classes.Experimenter import Experimenter
from Modules.Classes.ExpectedSolution import ExpectedSolution
from Modules.Classes.Measurement import Measurement
from Modules.Classes.Metric import Metric
from Modules.Classes.Pattern import Pattern
from Modules.Classes.PatternSection import PatternSection
from Modules.Classes.Problem import Problem
from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
from Modules.Classes.Report import Report
from Modules.Classes.Section import Section
from Modules.Classes.SentSolution import SentSolution
from Modules.Classes.Template import Template
from Modules.Classes.TemplateSection import TemplateSection

# Create tables in DB or access them if they exist
Base.metadata.create_all(engine)

# Create session with DB
session = Session()

# Create objects
metric_demo1 = Metric('Solution time', 'total time in seconds that the resolution of a problem lasts')
metric_demo2 = Metric('Selection time', 'time in seconds required to select a PDP solution')
metric_demo3 = Metric('Viewed patterns', 'total number of PDPs displayed')
metric_demo4 = Metric('Chosen patterns', 'number of PDPs added to the solution')

admin_demo = Administrator('Diego', 'Guzman', 'dguzman', hashlib.sha1('diego1234'.encode()).hexdigest())

experimenter_demo1 = Experimenter('Julio', 'Caiza', 'jcaiza', hashlib.sha1('jcaiza1234'.encode()).hexdigest())

# Make persistence in DB
session.add(admin_demo)
session.add(experimenter_demo1)
session.add(metric_demo1)
session.add(metric_demo2)
session.add(metric_demo3)
session.add(metric_demo4)

# Save changes and close connection
session.commit()
session.close()
