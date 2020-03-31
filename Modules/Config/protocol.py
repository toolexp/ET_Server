"""
File where all the possible actions of the server are defined. This file is called protocol, because it redirects
the server to an specific function depending on the action of the received message from the client.
"""

# Import all classes (entities) needed for the protocol (ALWAYS IMPORT ALL CLASSES MAPPED TO THE DATABASE, EVEN IF
# THEY ARE NOT USED, ALL CLASSES ARE NEEDED TO MAP WITH ALL ENTITIES CORRECTLY)
from Modules.Config.base import Session, engine, Base
from Modules.Classes.Administrator import Administrator
from Modules.Classes.Category import Category
from Modules.Classes.Classification import Classification
from Modules.Classes.Designer import Designer
from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
from Modules.Classes.Diagram import Diagram
from Modules.Classes.Experiment import Experiment
from Modules.Classes.ExperimentalScenario import ExperimentalScenario
from Modules.Classes.ExperimentalScenarioPattern import ExperimentalScenarioPattern
from Modules.Classes.Experimenter import Experimenter
from Modules.Classes.ExpectedSolution import ExpectedSolution
from Modules.Classes.Measurement import Measurement
from Modules.Classes.Metric import Metric
from Modules.Classes.Pattern import Pattern
from Modules.Classes.PatternSection import PatternSection
from Modules.Classes.Problem import Problem
from Modules.Classes.Report import Report
from Modules.Classes.Section import Section
from Modules.Classes.SentSolution import SentSolution
from Modules.Classes.Template import Template
from Modules.Classes.TemplateSection import TemplateSection


def handle_decision(message):
    """
    Function that chose the correct function depending on the message received

    :parameter message: message received from a client
    :type message: Modules.Config.Data.Message
    :return: message ready to send to a client (response of requested action)
    :rtype: Modules.Config.Data.Message
    """
    Base.metadata.create_all(engine)
    session = Session()
    argument = message.action
    func = switcher_protocol.get(argument, 'nothing')
    return func(message.information, session)


# Actual switch function that redirects server to chosen function (Modules.Config.Data.Message.action:Class.method)
switcher_protocol = {
    11: Administrator.create,
    12: Administrator.read,
    13: Administrator.update,
    14: Administrator.delete,
    15: Administrator.select,
    16: Experimenter.create,
    17: Experimenter.read,
    18: Experimenter.update,
    19: Experimenter.delete,
    20: Experimenter.select,
    21: Designer.create,
    22: Designer.read,
    23: Designer.update,
    24: Designer.delete,
    25: Designer.select,
    27: DesignerExperimentalScenario.read,
    29: DesignerExperimentalScenario.delete,
    31: Section.create,
    32: Section.read,
    33: Section.update,
    34: Section.delete,
    35: Section.select,
    36: Template.create,
    37: Template.read,
    38: Template.update,
    39: Template.delete,
    40: Template.select,
    41: Pattern.create,
    42: Pattern.read,
    44: Pattern.delete,
    45: Pattern.select,
    46: PatternSection.create,
    47: PatternSection.read,
    48: PatternSection.update,
    51: Problem.create,
    52: Problem.read,
    # 53: Problem.update,
    54: Problem.delete,
    55: Problem.select,
    56: ExpectedSolution.create,
    # 58: ExpectedSolution.update,
    # 59: ExpectedSolution.delete,
    60: ExpectedSolution.select,
    61: Diagram.create,
    63: Diagram.update,
    64: Diagram.delete,
    65: Diagram.select,
    66: Classification.create,
    67: Classification.read,
    68: Classification.update,
    69: Classification.delete,
    70: Classification.select,
    71: Category.create,
    72: Category.read,
    74: Category.delete,
    75: Category.select,
    77: TemplateSection.read,
    81: ExperimentalScenario.create,
    82: ExperimentalScenario.read,
    83: ExperimentalScenario.update,
    84: ExperimentalScenario.delete,
    85: ExperimentalScenario.select,
    87: ExperimentalScenarioPattern.read,
    89: ExperimentalScenarioPattern.delete,
    91: Experiment.create,
    92: Experiment.read,
    93: Experiment.update,
    94: Experiment.delete,
    95: Experiment.select,
    96: Measurement.create,
    101: SentSolution.create,
    # 102: SentSolution.read,
    # 103: SentSolution.update,
    # 104: SentSolution.delete,
    105: SentSolution.select,
    106: Report.create,
    107: Report.read
}
