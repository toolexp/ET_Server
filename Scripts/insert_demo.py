# coding=utf-8

# Import necessary modules
from datetime import date
from Modules.Config.base import Session, engine, Base

from Modules.Classes.Administrator import Administrator
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
from Modules.Classes.Section import Section
from Modules.Classes.SentSolution import SentSolution
from Modules.Classes.Template import Template

# Create tables in DB or access them if they exist
Base.metadata.create_all(engine)

# Create session with DB
session = Session()

# Create objects
admin_demo = Administrator('demo_name', 'demo_surname', 'demo_mail', 'demo_passwd')

designer_demo1 = Designer('demo_name', 'demo_surname', 'demo_mail', 'demo_passwd')
designer_demo2 = Designer('demo_name', 'demo_surname', 'demo_mail', 'demo_passwd')
designers_group_demo1 = DesignersGroup('demo_name', 'demo_description')
designers_group_demo2 = DesignersGroup('demo_name', 'demo_description')
designers_group_demo1.designers = [designer_demo1]
designers_group_demo2.designers = [designer_demo2]

experimenter_demo = Experimenter('demo_name', 'demo_surname', 'demo_mail', 'demo_passwd')
experiment_demo = Experiment('demo_name', 'demo_description')
experimenter_demo.experiments = [experiment_demo]

experimental_sc_demo = ExperimentalScenario('demo_name', 'demo_description', 'acces_code_demo', date(2000, 1, 1),
                                            date(2000, 1, 2), True, False, experiment_demo, designers_group_demo1,
                                            designers_group_demo2)

section_demo = Section('demo_name', 'demo_description', 'String', True)
template_demo = Template('demo_name', 'demo_description')
template_demo.sections = [section_demo]

diagram_demo = Diagram('demo_name', 'demo_file_path')
pattern_demo1 = Pattern('demo_name', template_demo, diagram_demo)
pattern_demo2 = Pattern('demo_name', template_demo, diagram_demo)
pattern_section = PatternSection('demo_content', pattern_demo1)
ideal_sol_demo = IdealSolution('demo_name', 'demo_description', diagram_demo)
ideal_sol_demo.patterns = [pattern_demo1, pattern_demo2]

problem_demo = Problem('demo_name', 'demo_description', ideal_sol_demo)
scenario_component_demo = ScenarioComponent(experimental_sc_demo, problem_demo)
scc_pattern_demo1 = ScenarioComponentPattern('demo_type1', scenario_component_demo, pattern_demo1)
scc_pattern_demo2 = ScenarioComponentPattern('demo_type2', scenario_component_demo, pattern_demo2)
sent_sol_demo = SentSolution('demo_name', 'demo_description', designer_demo1, scenario_component_demo, diagram_demo)

# Make persistence in DB
session.add(admin_demo)
session.add(designer_demo1)
session.add(designer_demo2)
session.add(designers_group_demo1)
session.add(designers_group_demo2)
session.add(experimenter_demo)
session.add(experiment_demo)
session.add(experimental_sc_demo)
session.add(section_demo)
session.add(template_demo)
session.add(diagram_demo)
session.add(pattern_demo1)
session.add(pattern_demo2)
session.add(pattern_section)
session.add(ideal_sol_demo)
session.add(problem_demo)
session.add(scenario_component_demo)
session.add(sent_sol_demo)
session.add(scc_pattern_demo1)
session.add(scc_pattern_demo2)

# Save changes and close connection
session.commit()
session.close()
