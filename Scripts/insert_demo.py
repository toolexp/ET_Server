# coding=utf-8

# Import necessary modules
from Modules.Config.base import Session, engine, Base
from Modules.Classes.Administrator import Administrator
from Modules.Classes.Category import Category
from Modules.Classes.Classification import Classification
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
from Modules.Classes.TemplateSection import TemplateSection

# Create tables in DB or access them if they exist

Base.metadata.create_all(engine)

# Create session with DB
session = Session()

# Create objects
admin_demo = Administrator('Juan', 'Perez', 'jperez@epn.ec', 'jperez1234')

designer_demo1 = Designer('Lorena', 'Zambrano', 'lzambrano@epn.ec', 'lzambrano1234')
designer_demo2 = Designer('Andrea', 'Rubio', 'arubio@epn.ec', 'arubio1234')
designer_demo3 = Designer('Ramiro', 'Valencia', 'rvalencia@epn.ec', 'rvalencia1234')
designer_demo4 = Designer('Camilo', 'Arteaga', 'carteaga@epn.ec', 'carteaga1234')

designers_group_demo1 = DesignersGroup('Alpha group', 'Group with skills in security')
designers_group_demo2 = DesignersGroup('Betta group', 'Group with skills in connectivity')

designers_group_demo1.designers = [designer_demo1, designer_demo3]
designers_group_demo2.designers = [designer_demo2, designer_demo4]

experimenter_demo1 = Experimenter('Natalia', 'Vargas', 'nvargas@epn.ec', 'nvargas1234')
experimenter_demo2 = Experimenter('Julian', 'Moreno', 'jmoreno@epn.ec', 'jmoreno1234')
experiment_demo = Experiment('Template 1 vs Template 2', 'Does using patterns of Template 1 reduce time vs using '
                                                         'patterns of Template 2?')
experimenter_demo1.experiments = [experiment_demo]
experimenter_demo2.experiments = [experiment_demo]

#experimental_sc_demo = ExperimentalScenario('demo_name', 'demo_description', 'acces_code_demo', date(2000, 1, 1),
                                            #date(2000, 1, 2), True, False, experiment_demo, designers_group_demo1,
                                            #designers_group_demo2)
classification_demo1 = Classification('Control')
category_demo1 = Category('Consent', classification_demo1)
category_demo2 = Category('Retract', classification_demo1)
category_demo3 = Category('Choose', classification_demo1)
category_demo4 = Category('Update', classification_demo1)

classification_demo2 = Classification('Abstract')
category_demo5 = Category('Abstract', classification_demo2)

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
section_demo6 = Section(classification_demo1.name, 'NA', 'Classification', classification_demo1)
section_demo7 = Section('Name', 'Text that describes the pattern', 'Text', None)

template_demo1 = Template('Control template', 'Not defined')
template_demo2 = Template('Inform template', 'Not defined')
template_demo3 = Template('Enforce template', 'Not defined')

t1_section1 = TemplateSection(True, 2, template_demo1, section_demo1)
t1_section2 = TemplateSection(True, 3, template_demo1, section_demo2)
t1_section3 = TemplateSection(True, 4, template_demo1, section_demo3)
t1_section4 = TemplateSection(True, 1, template_demo1, section_demo7)

t2_section1 = TemplateSection(True, 2, template_demo2, section_demo1)
t2_section2 = TemplateSection(True, 3, template_demo2, section_demo2)
t2_section3 = TemplateSection(False, 4, template_demo2, section_demo3)
t2_section4 = TemplateSection(True, 5, template_demo2, section_demo4)
t2_section5 = TemplateSection(False, 6, template_demo2, section_demo5)
t2_section6 = TemplateSection(True, 1, template_demo2, section_demo7)

t3_section1 = TemplateSection(True, 2, template_demo3, section_demo1)
t3_section2 = TemplateSection(True, 3, template_demo3, section_demo2)
t3_section3 = TemplateSection(True, 4, template_demo3, section_demo6)
t3_section4 = TemplateSection(True, 1, template_demo3, section_demo7)

diagram_demo = Diagram('diagram_demo.jpg', './Resources/Diagrams/diagram_demo.jpg')

pattern_demo1 = Pattern(template_demo1)
pattern_demo2 = Pattern(template_demo2)
pattern_demo3 = Pattern(template_demo3)

pattern_section1 = PatternSection('User wants to store or transfer their personal data through an online service and '
                                  'they want to protect their privacy, and specifically the confidentiality of their '
                                  'personal information. Risks of unauthorized access may include the online service '
                                  'provider itself, or third parties such as its partners for example for backup, or '
                                  'government surveillance depending on the geographies the data is stored in or '
                                  'transferred through.', pattern_demo1, t1_section1, None, None)
pattern_section2 = PatternSection('How can a user store or transfer their personal information through an online '
                                  'service while ensuring their privacy and specifically preventing unauthorized '
                                  'access to their personal information? '
                                  'Requiring the user to do encryption key management may annoy or confuse them and '
                                  'they may revert to either no encryption, or encryption with the online service '
                                  'provider managing the encryption key (affording no protection from the specific '
                                  'online service provider managing the key), picking an encryption key that is weak, '
                                  'reused, written down and so forth. Some metadata may need to remain unencrypted to '
                                  'support the online service provider or 3rd party functions, for example file names '
                                  'for cloud storage, or routing information for transfer applications, exposing the '
                                  'metadata to risks of unauthorized access, server side indexing for searching, '
                                  'or de-duplication. If the service provider has written the client side software that '
                                  'does the client side encryption with a user-managed encryption key, there can be '
                                  'additional concerns regarding whether the client software is secure or tampered with '
                                  'in ways that can compromise privacy.', pattern_demo1, t1_section2, None, None)
pattern_section3 = PatternSection('Encryption of the personal information of the user prior to storing it with, or '
                                  'transferring it through an online service. In this solution the user shall generate '
                                  'a strong encryption key and manage it themselves, specifically keeping it private and '
                                  'unknown to the untrusted online service or 3rd parties.', pattern_demo1, t1_section3,
                                  None, None)
pattern_section11 = PatternSection('Encryption with user-managed keys', pattern_demo1, t1_section4, None, None)

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

pattern_section9 = PatternSection('Machine-readable policies are sticked to data to define allowed usage and obligations '
                                  'as it travels across multiple parties, enabling users to improve control over their '
                                  'personal information.''', pattern_demo3, t3_section1, None, None)
pattern_section10 = PatternSection('Beneﬁts: Policies can be propagated throughout the cloud to trusted organisations, '
                                   'strong enforcement of the policies, traceability. Liabilities: Scalability: policies '
                                   'increase size of data. Practicality may not be compatible with existing systems. '
                                   'It may be difficult to update the policy after sharing of the data and existence '
                                   'of multiple copies of data. It requires ensuring data is handled according to '
                                   'policy e.g. using auditing.', pattern_demo3, t3_section2, None, None)
pattern_section13 = PatternSection('<' + category_demo2.name + '>', pattern_demo3, t3_section3, None, category_demo2)
pattern_section14 = PatternSection('Sticky Policies', pattern_demo3, t3_section4, None, None)

ideal_sol_demo = IdealSolution('demo_annotation', diagram_demo)
ideal_sol_demo.patterns = [pattern_demo1, pattern_demo2]

problem_demo = Problem('demo_name', 'demo_description', ideal_sol_demo)
#scenario_component_demo = ScenarioComponent(experimental_sc_demo, problem_demo)
#scc_pattern_demo1 = ScenarioComponentPattern('demo_type1', scenario_component_demo, pattern_demo1)
#scc_pattern_demo2 = ScenarioComponentPattern('demo_type2', scenario_component_demo, pattern_demo2)
#sent_sol_demo = SentSolution('demo_name', 'demo_description', designer_demo1, scenario_component_demo, diagram_demo)

# Make persistence in DB
session.add(admin_demo)
session.add(designer_demo1)
session.add(designer_demo2)
session.add(designer_demo3)
session.add(designer_demo4)
session.add(designers_group_demo1)
session.add(designers_group_demo2)
session.add(experimenter_demo1)
session.add(experimenter_demo2)
session.add(experiment_demo)
#session.add(experimental_sc_demo)
session.add(classification_demo1)
session.add(category_demo1)
session.add(category_demo2)
session.add(category_demo3)
session.add(category_demo4)
session.add(classification_demo2)
session.add(category_demo5)

session.add(section_demo1)
session.add(section_demo2)
session.add(section_demo3)
session.add(section_demo4)
session.add(section_demo5)
session.add(section_demo6)
session.add(section_demo7)

session.add(template_demo1)
session.add(template_demo2)
session.add(template_demo3)
session.add(t1_section1)
session.add(t1_section2)
session.add(t1_section3)
session.add(t1_section4)
session.add(t2_section1)
session.add(t2_section2)
session.add(t2_section3)
session.add(t2_section4)
session.add(t2_section5)
session.add(t2_section6)
session.add(t3_section1)
session.add(t3_section2)
session.add(t3_section3)
session.add(t3_section4)
session.add(diagram_demo)
session.add(pattern_demo1)
session.add(pattern_demo2)
session.add(pattern_demo3)
session.add(pattern_section1)
session.add(pattern_section2)
session.add(pattern_section3)
session.add(pattern_section4)
session.add(pattern_section5)
session.add(pattern_section6)
session.add(pattern_section7)
session.add(pattern_section8)
session.add(pattern_section9)
session.add(pattern_section10)
session.add(pattern_section11)
session.add(pattern_section12)
session.add(pattern_section13)
session.add(pattern_section14)
session.add(ideal_sol_demo)
session.add(problem_demo)
#session.add(scenario_component_demo)
#session.add(sent_sol_demo)
#session.add(scc_pattern_demo1)
#session.add(scc_pattern_demo2)

# Save changes and close connection
session.commit()
session.close()
