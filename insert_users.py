"""
Script that insert values for users(administrators and experimenters) to the database. This is necessary to be ran if
insert_demo.py script is not executed, so at least one user is registered in the system. This script also creates the
default metrics. This script may be ran once if needed before working with the project
"""

# Import necessary modules
import hashlib
from datetime import datetime

# Import all classes (ALWAYS IMPORT ALL CLASSES MAPPED TO THE DATABASE, EVEN IF THEY ARE NOT USED, NEEDED TO MAP ALL
# CLASSES WITH ALL ENTITIES CORRECTLY)
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
metric_demo1 = Metric(1, 'Solution time', 'total time in seconds that the resolution of a problem lasts')
metric_demo2 = Metric(2, 'Selection time', 'time in seconds required to select a PDP solution')
metric_demo3 = Metric(3, 'Viewed patterns', 'total number of PDPs displayed')
metric_demo4 = Metric(4, 'Chosen patterns', 'number of PDPs added to the solution')

admin_demo = Administrator('Diego', 'Guzman', 'dguzman', hashlib.sha1('diego1234'.encode()).hexdigest())

experimenter_demo1 = Experimenter('Julio', 'Caiza', 'jcaiza', hashlib.sha1('jcaiza1234'.encode()).hexdigest())
experimenter_demo2 = Experimenter('Zaida', 'Andrade', 'zandrade', hashlib.sha1('zandrade1234'.encode()).hexdigest())

# Make persistence in DB
session.add(admin_demo)
session.add(experimenter_demo1)
session.add(experimenter_demo2)
session.add(metric_demo1)
session.add(metric_demo2)
session.add(metric_demo3)
session.add(metric_demo4)

# Save changes and close connection
session.commit()
session.close()
