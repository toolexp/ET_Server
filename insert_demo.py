"""
Script that insert demo values for most of the entities of the database. This script may be ran once if needed before
working with the project
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

experiment_demo = Experiment('Template 1 vs Template 2', 'Does using patterns of Template 1 reduce time vs using '
                                                         'patterns of Template 2?', 2)
experimenter_demo1.experiments = [experiment_demo]

designer_demo1 = Designer('dp1', 'na', 'dp1', hashlib.sha1('dp11234'.encode()).hexdigest())
designer_demo2 = Designer('dp2', 'na', 'dp2', hashlib.sha1('dp21234'.encode()).hexdigest())
designer_demo3 = Designer('dp3', 'na', 'dp3', hashlib.sha1('dp31234'.encode()).hexdigest())
designer_demo4 = Designer('dp4', 'na', 'dp4', hashlib.sha1('dp41234'.encode()).hexdigest())
designer_demo5 = Designer('dp5', 'na', 'dp5', hashlib.sha1('dp51234'.encode()).hexdigest())
designer_demo6 = Designer('dp6', 'na', 'dp6', hashlib.sha1('dp61234'.encode()).hexdigest())
designer_demo7 = Designer('dp7', 'na', 'dp7', hashlib.sha1('dp71234'.encode()).hexdigest())
designer_demo8 = Designer('dp8', 'na', 'dp8', hashlib.sha1('dp81234'.encode()).hexdigest())
designer_demo9 = Designer('dp9', 'na', 'dp9', hashlib.sha1('dp91234'.encode()).hexdigest())
designer_demo10 = Designer('dp10', 'na', 'dp10', hashlib.sha1('dp101234'.encode()).hexdigest())
designer_demo11 = Designer('dp11', 'na', 'dp11', hashlib.sha1('dp111234'.encode()).hexdigest())
designer_demo12 = Designer('dp12', 'na', 'dp12', hashlib.sha1('dp121234'.encode()).hexdigest())
designer_demo13 = Designer('dp13', 'na', 'dp13', hashlib.sha1('dp131234'.encode()).hexdigest())
designer_demo14 = Designer('dp14', 'na', 'dp14', hashlib.sha1('dp141234'.encode()).hexdigest())
designer_demo15 = Designer('dp15', 'na', 'dp15', hashlib.sha1('dp151234'.encode()).hexdigest())
designer_demo16 = Designer('dp16', 'na', 'dp16', hashlib.sha1('dp161234'.encode()).hexdigest())
designer_demo17 = Designer('dp17', 'na', 'dp17', hashlib.sha1('dp171234'.encode()).hexdigest())
designer_demo18 = Designer('dp18', 'na', 'dp18', hashlib.sha1('dp181234'.encode()).hexdigest())
designer_demo19 = Designer('dp19', 'na', 'dp19', hashlib.sha1('dp191234'.encode()).hexdigest())
designer_demo20 = Designer('dp20', 'na', 'dp20', hashlib.sha1('dp201234'.encode()).hexdigest())

classification_demo1 = Classification('Control')
category_demo1 = Category('Consent', classification_demo1)
category_demo2 = Category('Retract', classification_demo1)
category_demo3 = Category('Choose', classification_demo1)
category_demo4 = Category('Update', classification_demo1)

section_demo1 = Section('Context', 'It establishes the parameters of the situation in which the problem arises. '
                                   'Explain '
                                   'how these can influence the problem and the repercussions they will have on the '
                                   'solution.', 'Text', None)
section_demo2 = Section('Problem', 'It presents the problem to be solved, without factors that influence its '
                                   'definition '
                                   'or possible solution.', 'Text', None)
section_demo3 = Section('Solution', 'The solution proposed for the proposed problem.', 'Text', None)
section_demo4 = Section('Consequences', 'Direct and indirect, positive and negative consequences after the application '
                                        'of the proposed solution.', 'Text', None)
section_demo5 = Section('Diagram', 'Schematic representation of the pattern', 'File', None)
section_demo7 = Section('Name', 'Text that describes the pattern', 'Text', None)

template_demo2 = Template('Inform template', 'Not defined')

t2_section1 = TemplateSection(True, 2, False, template_demo2, section_demo1)
t2_section2 = TemplateSection(True, 3, False, template_demo2, section_demo2)
t2_section3 = TemplateSection(False, 4, False, template_demo2, section_demo3)
t2_section4 = TemplateSection(True, 5, False, template_demo2, section_demo4)
t2_section5 = TemplateSection(False, 6, False, template_demo2, section_demo5)
t2_section6 = TemplateSection(True, 1, True, template_demo2, section_demo7)

diagram_demo = Diagram('diagram_demo.jpg', './Resources/Diagrams/Patterns/diagram_demo.jpg')

pattern_demo2 = Pattern(template_demo2)

pattern_section4 = PatternSection('Credentials are required by numerous services (and products) in order to ensure that '
                                  'only authenticated and authorized users have access to certain features. Controllers '
                                  'typically provide authentication mechanisms in the form of usernames and passwords. '
                                  'Although these provide a weak form of security when used incorrectly, they are more '
                                  'convenient for users than many less popular and more secure alternatives. '
                                  'Controllers often try to circumvent the shortcomings of passwords by encouraging '
                                  'users to change them frequently, use stronger variations, check them, and prevent '
                                  'disclosure and reuse. However users make use of many services, and use many '
                                  'passwords, thus discouraging proper application. This misapplication can result in '
                                  'personal data being accessed by unauthorized persons.', pattern_demo2, t2_section1,
                                  None, None)
pattern_section5 = PatternSection('Users must regularly maintain many strong passwords, remember them, and protect them, '
                                  'but are not well equipped to do so. So instead many choose weak ones and reuse them.',
                                  pattern_demo2, t2_section2, None, None)
pattern_section6 = PatternSection('Provide users with assistance in understanding and maintaining strong passwords which '
                                  'are easier to remember.', pattern_demo2, t2_section3, None, None)
pattern_section7 = PatternSection('Secure passwords are very important in [an interconnected world]. Users generally '
                                  'tend to use familiar words such as names of pets and family members and no special '
                                  '[characters] when creating a password. These passwords can hence be easier hacked '
                                  'using social engineering than longer [and more complex passwords]. Secure passwords '
                                  'are a necessary step towards personal security. Using the above approach, the user '
                                  'obtains more feedback on the safety of the entered password and is therefore able to '
                                  'create safe passwords that can be remembered.', pattern_demo2, t2_section4, None, None)
pattern_section8 = PatternSection('<File>', pattern_demo2, t2_section5, diagram_demo, None)
pattern_section12 = PatternSection('Informed Secure Passwords', pattern_demo2, t2_section6, None, None)

diagram_demo2 = Diagram('diagram_demo.jpg', './Resources/Diagrams/ExpectedSolution/diagram_demo.jpg')

expected_sol_demo2 = ExpectedSolution('No requiered annotations', diagram_demo2)
expected_sol_demo2.patterns = [pattern_demo2]

diagram_demo3 = Diagram('diagram_demo.jpg', './Resources/Diagrams/ContextDiagram/diagram_demo.jpg')
experimental_sc_demo = ExperimentalScenario('Experimental scenario 1', 'NA', '1234567890', 'created', diagram_demo3,
                                            experiment_demo)

problem_demo1 = Problem('Software that is difficult to use', 'Many people have experienced first-hand the frustration of '
                                                            'using software that is cumbersome, difficult to navigate, '
                                                            'and requires several steps to perform simple tasks.',
                        expected_sol_demo2, experimental_sc_demo)

des_exp_sc_demo1 = DesignerExperimentalScenario(1, designer_demo1, experimental_sc_demo)
des_exp_sc_demo2 = DesignerExperimentalScenario(1, designer_demo2, experimental_sc_demo)
des_exp_sc_demo3 = DesignerExperimentalScenario(1, designer_demo3, experimental_sc_demo)
des_exp_sc_demo4 = DesignerExperimentalScenario(1, designer_demo4, experimental_sc_demo)
des_exp_sc_demo5 = DesignerExperimentalScenario(1, designer_demo5, experimental_sc_demo)
des_exp_sc_demo6 = DesignerExperimentalScenario(1, designer_demo6, experimental_sc_demo)
des_exp_sc_demo7 = DesignerExperimentalScenario(1, designer_demo7, experimental_sc_demo)
des_exp_sc_demo8 = DesignerExperimentalScenario(1, designer_demo8, experimental_sc_demo)
des_exp_sc_demo9 = DesignerExperimentalScenario(1, designer_demo9, experimental_sc_demo)
des_exp_sc_demo10 = DesignerExperimentalScenario(1, designer_demo10, experimental_sc_demo)
des_exp_sc_demo11 = DesignerExperimentalScenario(2, designer_demo11, experimental_sc_demo)
des_exp_sc_demo12 = DesignerExperimentalScenario(2, designer_demo12, experimental_sc_demo)
des_exp_sc_demo13 = DesignerExperimentalScenario(2, designer_demo13, experimental_sc_demo)
des_exp_sc_demo14 = DesignerExperimentalScenario(2, designer_demo14, experimental_sc_demo)
des_exp_sc_demo15 = DesignerExperimentalScenario(2, designer_demo15, experimental_sc_demo)
des_exp_sc_demo16 = DesignerExperimentalScenario(2, designer_demo16, experimental_sc_demo)
des_exp_sc_demo17 = DesignerExperimentalScenario(2, designer_demo17, experimental_sc_demo)
des_exp_sc_demo18 = DesignerExperimentalScenario(2, designer_demo18, experimental_sc_demo)
des_exp_sc_demo19 = DesignerExperimentalScenario(2, designer_demo19, experimental_sc_demo)
des_exp_sc_demo20 = DesignerExperimentalScenario(2, designer_demo20, experimental_sc_demo)

exp_sc_pat_demo1 = ExperimentalScenarioPattern(1, experimental_sc_demo, pattern_demo2)
exp_sc_pat_demo2 = ExperimentalScenarioPattern(2, experimental_sc_demo, pattern_demo2)

# Make persistence in DB
session.add(admin_demo)
session.add(designer_demo1)
session.add(designer_demo2)
session.add(designer_demo3)
session.add(designer_demo4)
session.add(designer_demo5)
session.add(designer_demo6)
session.add(designer_demo7)
session.add(designer_demo8)
session.add(designer_demo9)
session.add(designer_demo10)
session.add(designer_demo11)
session.add(designer_demo12)
session.add(designer_demo13)
session.add(designer_demo14)
session.add(designer_demo15)
session.add(designer_demo16)
session.add(designer_demo17)
session.add(designer_demo18)
session.add(designer_demo19)
session.add(designer_demo20)
session.add(experimenter_demo1)
session.add(experimenter_demo2)
session.add(metric_demo1)
session.add(metric_demo2)
session.add(metric_demo3)
session.add(metric_demo4)
session.add(experiment_demo)
session.add(classification_demo1)
session.add(category_demo1)
session.add(category_demo2)
session.add(category_demo3)
session.add(category_demo4)
session.add(section_demo1)
session.add(section_demo2)
session.add(section_demo3)
session.add(section_demo4)
session.add(section_demo5)
session.add(section_demo7)
session.add(template_demo2)
session.add(t2_section1)
session.add(t2_section2)
session.add(t2_section3)
session.add(t2_section4)
session.add(t2_section5)
session.add(t2_section6)
session.add(diagram_demo)
session.add(diagram_demo2)
session.add(diagram_demo3)
session.add(pattern_demo2)
session.add(pattern_section4)
session.add(pattern_section5)
session.add(pattern_section6)
session.add(pattern_section7)
session.add(pattern_section8)
session.add(pattern_section12)
session.add(expected_sol_demo2)
session.add(experimental_sc_demo)
session.add(problem_demo1)
session.add(des_exp_sc_demo1)
session.add(des_exp_sc_demo2)
session.add(des_exp_sc_demo3)
session.add(des_exp_sc_demo4)
session.add(des_exp_sc_demo5)
session.add(des_exp_sc_demo6)
session.add(des_exp_sc_demo7)
session.add(des_exp_sc_demo8)
session.add(des_exp_sc_demo9)
session.add(des_exp_sc_demo10)
session.add(des_exp_sc_demo11)
session.add(des_exp_sc_demo12)
session.add(des_exp_sc_demo13)
session.add(des_exp_sc_demo14)
session.add(des_exp_sc_demo15)
session.add(des_exp_sc_demo16)
session.add(des_exp_sc_demo17)
session.add(des_exp_sc_demo18)
session.add(des_exp_sc_demo19)
session.add(des_exp_sc_demo20)
session.add(exp_sc_pat_demo1)
session.add(exp_sc_pat_demo2)

# Save changes and close connection
session.commit()
session.close()
