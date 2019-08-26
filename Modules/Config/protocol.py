# coding=utf-8

# Import necessary modules
from datetime import date
from Modules.Config.base import Session, engine, Base
from Modules.Config.Message import Message
from Modules.Classes.Administrator import Administrator
from Modules.Classes.Section import Section
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


def handle_decision(message, socket):
    if message.comment == 'close_connection':
        socket.close()
    Base.metadata.create_all(engine)
    session = Session()
    argument = message.action
    func = switcher_protocol.get(argument, 'nothing')
    return func(message.information, session)


def create_admin(parameters, session):
    """
    Creates an 'Administrator' object and stores it into the database, the data for the
    object is inside the 'parameters'

    Parameters
    ----------
    parameters: Message.information []
        List of data (string, int, boolean, list, etc) that contains information
        -> parameters[0] has Administrator.name
        -> parameters[1] has Administrator.surname
        -> parameters[2] has Administrator.email
        -> parameters[3] has Administrator.password
    session: Session
        Session with connection to the database
    Returns
    -------
    msg_rspt: Message
        Message with information of the fail or success of the operation

    Raises
    ------
    Exception:
        If any of the lines of code generates an error
    """
    admin_aux = Administrator(parameters[0], parameters[1], parameters[2], parameters[3])
    session.add(admin_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_admin(parameters, session):
    admins = session.query(Administrator).all()
    session.close()
    msg_rspt = Message(action=2, information=[])
    for admin in admins:
        msg_rspt.information.append(admin.__str__())
    return msg_rspt


def update_admin(parameters, session):
    admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
    admin_aux.name = parameters[1]
    admin_aux.surname = parameters[2]
    admin_aux.email = parameters[3]
    admin_aux.password = parameters[4]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_admin(parameters, session):
    admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
    session.delete(admin_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_admin(parameters, session):
    admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
    session.close()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(admin_aux.name)
    msg_rspt.information.append(admin_aux.surname)
    msg_rspt.information.append(admin_aux.email)
    msg_rspt.information.append(admin_aux.password)
    return msg_rspt


def create_experimenter(parameters, session):
    experimenter_aux = Experimenter(parameters[0], parameters[1], parameters[2], parameters[3])
    session.add(experimenter_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_experimenter(parameters, session):
    experimenters = session.query(Experimenter).all()
    session.close()
    msg_rspt = Message(action=2, information=[])
    for experimenter in experimenters:
        msg_rspt.information.append(experimenter.__str__())
    return msg_rspt


def update_experimenter(parameters, session):
    experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
    experimenter_aux.name = parameters[1]
    experimenter_aux.surname = parameters[2]
    experimenter_aux.email = parameters[3]
    experimenter_aux.password = parameters[4]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_experimenter(parameters, session):
    experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
    session.delete(experimenter_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_experimenter(parameters, session):
    experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
    session.close()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(experimenter_aux.name)
    msg_rspt.information.append(experimenter_aux.surname)
    msg_rspt.information.append(experimenter_aux.email)
    msg_rspt.information.append(experimenter_aux.password)
    return msg_rspt


def create_designer(parameters, session):
    designer_aux = Designer(parameters[0], parameters[1], parameters[2], parameters[3])
    session.add(designer_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_designer(parameters, session):
    designers = session.query(Designer).all()
    session.close()
    msg_rspt = Message(action=2, information=[])
    for designer in designers:
        msg_rspt.information.append(designer.__str__())
    return msg_rspt


def update_designer(parameters, session):
    designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
    designer_aux.name = parameters[1]
    designer_aux.surname = parameters[2]
    designer_aux.email = parameters[3]
    designer_aux.password = parameters[4]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_designer(parameters, session):
    designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
    session.delete(designer_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_designer(parameters, session):
    designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
    session.close()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(designer_aux.name)
    msg_rspt.information.append(designer_aux.surname)
    msg_rspt.information.append(designer_aux.email)
    msg_rspt.information.append(designer_aux.password)
    return msg_rspt


def create_designers_group(parameters, session):
    designers_group_aux = DesignersGroup(parameters[0], parameters[1])
    for i in range(0,len(parameters[2])):
        designer_aux = session.query(Designer).filter(Designer.id == parameters[2][i]).first()
        designers_group_aux.designers += [designer_aux]
    session.add(designers_group_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_designers_group(parameters, session):
    designers_groups = session.query(DesignersGroup).all()
    msg_rspt = Message(action=2, information=[])
    for designer_group in designers_groups:
        msg_rspt.information.append(designer_group.__str__())
    session.close()
    return msg_rspt


def update_designers_group(parameters, session):
    designers_group_aux = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[0]).first()
    designers_group_aux.name = parameters[1]
    designers_group_aux.description = parameters[2]
    designers_group_aux.designers = []
    for i in range(0,len(parameters[3])):
        designer_aux = session.query(Designer).filter(Designer.id == parameters[3][i]).first()
        designers_group_aux.designers += [designer_aux]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_designers_group(parameters, session):
    designers_group_aux = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[0]).first()
    session.delete(designers_group_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_designers_group(parameters, session):
    designers_group_aux = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(designers_group_aux.name)
    msg_rspt.information.append(designers_group_aux.description)
    msg_rspt.information.append([])
    for i in range(0, len(designers_group_aux.designers)):
        msg_rspt.information[2].append(designers_group_aux.designers[i].__str__())
    session.close()
    return msg_rspt


def create_section(parameters, session):
    section_aux = Section(parameters[0], parameters[1], parameters[2], parameters[3])
    session.add(section_aux)
    session.commit()
    section_aux = session.query(Section).order_by(Section.id.desc()).first()
    session.close()
    msg_rspt = Message(action=2, information=[section_aux.__str__()], comment='Register created successfully')
    return msg_rspt


def read_section(parameters, session):
    sections = session.query(Section).all()
    msg_rspt = Message(action=2, information=[])
    for section in sections:
        msg_rspt.information.append(section.__str__())
    session.close()
    return msg_rspt


def update_section(parameters, session):
    section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
    section_aux.name = parameters[1]
    section_aux.description = parameters[2]
    section_aux.data_type = parameters[3]
    section_aux.mandatory = parameters[4]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_section(parameters, session):
    section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
    session.delete(section_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_section(parameters, session):
    section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(section_aux.name)
    msg_rspt.information.append(section_aux.description)
    msg_rspt.information.append(section_aux.data_type)
    msg_rspt.information.append(section_aux.mandatory)
    session.close()
    return msg_rspt


def create_template(parameters, session):
    template_aux = Template(parameters[0], parameters[1])
    for i in range(0,len(parameters[2])):
        section_aux = session.query(Section).filter(Section.id == parameters[2][i]).first()
        template_aux.sections += [section_aux]
    session.add(template_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_template(parameters, session):
    templates = session.query(Template).all()
    msg_rspt = Message(action=2, information=[])
    for template in templates:
        msg_rspt.information.append(template.__str__())
    session.close()
    return msg_rspt


def update_template(parameters, session):
    template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
    template_aux.name = parameters[1]
    template_aux.description = parameters[2]
    template_aux.sections = []
    for i in range(0,len(parameters[3])):
        section_aux = session.query(Section).filter(Section.id == parameters[3][i]).first()
        template_aux.sections += [section_aux]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_template(parameters, session):
    template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
    session.delete(template_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_template(parameters, session):
    # Received --> parameters = [id_template]
    # Return --> msg_rspt = [2, '', [template_name, template_description, [section1._str_(), section2._str_(), ...]]]
    template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(template_aux.name)
    msg_rspt.information.append(template_aux.description)
    msg_rspt.information.append([])
    for i in range(0, len(template_aux.sections)):
        msg_rspt.information[2].append(template_aux.sections[i].__str__())
    session.close()
    return msg_rspt


'''def create_pattern(parameters, session):
    template_aux = session.query(Template).filter(Template.id == parameters[1]).first()
    if len(parameters) == 2:
        # Without diagram --> parameters=[name, id_Template]
        pattern_aux = Pattern(parameters[0], template_aux, None)
    else:
        # With diagram --> parameters=[name, id_Template, id_Diagram]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
        pattern_aux = Pattern(parameters[0], template_aux, diagram_aux)
    session.add(pattern_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt'''

def create_pattern(parameters, session):
    template_aux = session.query(Template).filter(Template.id == parameters[1]).first()
    pattern_aux = Pattern(parameters[0], template_aux)
    session.add(pattern_aux)
    session.commit()
    id_pattern_aux = session.query(Pattern).order_by(Pattern.id.desc()).first()
    session.close()
    msg_rspt = Message(action=2, information=[id_pattern_aux.id], comment='Register created successfully')
    return msg_rspt



def read_pattern(parameters, session):
    patterns = session.query(Pattern).all()
    msg_rspt = Message(action=2, information=[])
    for pattern in patterns:
        msg_rspt.information.append(pattern.__str__())
    session.close()
    return msg_rspt


def update_pattern(parameters, session):
    # Received --> [id_pattern, name]
    # Template can not be updated
    pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
    pattern_aux.name = parameters[1]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt

'''def update_pattern(parameters, session):
    # Without diagram parameters = [id_pattern, name, id_template]
    pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
    template_aux = session.query(Template).filter(Template.id == parameters[2]).first()
    pattern_aux.name = parameters[1]
    pattern_aux.template = template_aux
    if len(parameters) == 4:
        # With diagram parameters = [id_pattern, name, id_template, id_diagram]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
        pattern_aux.diagram = diagram_aux
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt'''


def delete_pattern(parameters, session):
    pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
    session.delete(pattern_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_pattern(parameters, session):
    pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(pattern_aux.name)
    msg_rspt.information.append(pattern_aux.template.__str__())
    '''if pattern_aux.diagram is not None:
        msg_rspt.information.append(pattern_aux.diagram.__str__())'''
    session.close()
    return msg_rspt


def create_content(parameters, session):
    # Received --> [content, id_pattern, id_section, id_diagram]
    pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[1]).first()
    section_aux = session.query(Section).filter(Section.id == parameters[2]).first()
    if parameters[3] is not None:
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
    else:
        diagram_aux = None
    content_aux = PatternSection(parameters[0], pattern_aux, section_aux, diagram_aux)
    session.add(content_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_content(parameters, session):
    # Received --> [id_Pattern]
    contents = session.query(PatternSection).filter(PatternSection.pattern_id == parameters[0]).all()
    msg_rspt = Message(action=2, information=[])
    for content in contents:
        msg_rspt.information.append(content.__str__())
    session.close()
    return msg_rspt


def update_content(parameters, session):
    # Received --> [id_pattern_section, content, id_diagram]
    content_aux = session.query(PatternSection).filter(PatternSection.id == parameters[0]).first()
    content_aux.content = parameters[1]
    if parameters[2] is not None:
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
    else:
        diagram_aux = None
    content_aux.diagram = diagram_aux
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_content(parameters, session):
    # Received --> [id_pattern_section]
    content_aux = session.query(PatternSection).filter(PatternSection.id == parameters[0]).first()
    session.delete(content_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


'''def select_content(parameters, session):
    pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(pattern_aux.name)
    msg_rspt.information.append(pattern_aux.template.__str__())
    if pattern_aux.diagram is not None:
        msg_rspt.information.append(pattern_aux.diagram.__str__())
    session.close()
    return msg_rspt'''


def create_problem(parameters, session):
    # First create the ideal solution
    # Received --> [name, description, id_i_solution]
    solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[2]).first()
    problem_aux = Problem(parameters[0], parameters[1], solution_aux)
    session.add(problem_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_problem(parameters, session):
    problems = session.query(Problem).all()
    msg_rspt = Message(action=2, information=[])
    for problem in problems:
        msg_rspt.information.append(problem.__str__())
    session.close()
    return msg_rspt


def update_problem(parameters, session):
    # Received --> [id_problem, name, description, id_i_solution]
    problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
    i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[3]).first()
    problem_aux.name = parameters[1]
    problem_aux.description = parameters[2]
    problem_aux.ideal_solution = i_solution_aux
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_problem(parameters, session):
    # Received --> [id_problem]
    problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
    session.delete(problem_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_problem(parameters, session):
    # Received --> [id_problem]
    problem_aux = session.query(Problem).filter(Problem.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(problem_aux.name)
    msg_rspt.information.append(problem_aux.description)
    msg_rspt.information.append(problem_aux.ideal_solution_id)
    session.close()
    return msg_rspt


def create_i_solution(parameters, session):
    if len(parameters) == 3:
        if parameters[2] is not list:
            # Wthout patterns --> parameters=[name, description, id_diagram]
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
            i_solution_aux = IdealSolution(parameters[0], parameters[1], diagram_aux)
        else:
            # Without diagram --> parameters=[name, description, [id_pattern1, id_pattern2, ...]]
            i_solution_aux = IdealSolution(parameters[0], parameters[1], None)
            i_solution_aux.patterns = []
            for i in range(0, len(parameters[2])):
                pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[2][i]).first()
                i_solution_aux.patterns += pattern_aux
    else:
        # With diagram and patterns--> parameters=[name, description, id_diagram, [id_pattern1, id_pattern2, ...]]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
        i_solution_aux = IdealSolution(parameters[0], parameters[1], diagram_aux)
        i_solution_aux.patterns = []
        for i in range(0, len(parameters[2])):
            pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[2][i]).first()
            i_solution_aux.patterns += pattern_aux
    session.add(i_solution_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


'''def read_i_solution(parameters, session):
    templates = session.query(Template).all()
    msg_rspt = Message(action=2, information=[])
    for template in templates:
        msg_rspt.information.append(template.__str__())
    session.close()
    return msg_rspt'''


def update_i_solution(parameters, session):
    if len(parameters) == 4:
        if parameters[3] is not list:
            # Wthout patterns --> parameters=[id_i_solution, name, description, id_diagram]
            i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
            diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
            i_solution_aux.name = parameters[1]
            i_solution_aux.description = parameters[2]
            i_solution_aux.diagram = diagram_aux
        else:
            # Without diagram --> parameters=[id_i_solution, name, description, [id_pattern1, id_pattern2, ...]]
            i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
            i_solution_aux.name = parameters[1]
            i_solution_aux.description = parameters[2]
            i_solution_aux.patterns = []
            for i in range(0, len(parameters[3])):
                pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[3][i]).first()
                i_solution_aux.patterns += pattern_aux
    else:
        # With diagram and patterns--> parameters=[id_i_solution, name, description, id_diagram, [id_pattern1, id_pattern2, ...]]
        i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
        i_solution_aux.name = parameters[1]
        i_solution_aux.description = parameters[2]
        i_solution_aux.diagram = diagram_aux
        i_solution_aux.patterns = []
        for i in range(0, len(parameters[4])):
            pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[4][i]).first()
            i_solution_aux.patterns += pattern_aux
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def delete_i_solution(parameters, session):
    i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
    session.delete(i_solution_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_i_solution(parameters, session):
    i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(i_solution_aux.name)
    msg_rspt.information.append(i_solution_aux.description)
    msg_rspt.information.append(i_solution_aux.diagram_id)
    msg_rspt.information.append([])
    for i in range(0, len(i_solution_aux.patterns)):
        msg_rspt.information[2].append(i_solution_aux.patterns[i].__str__())
    session.close()
    return msg_rspt


switcher_protocol = {
        11: create_admin,
        12: read_admin,
        13: update_admin,
        14: delete_admin,
        15: select_admin,
        16: create_experimenter,
        17: read_experimenter,
        18: update_experimenter,
        19: delete_experimenter,
        20: select_experimenter,
        21: create_designer,
        22: read_designer,
        23: update_designer,
        24: delete_designer,
        25: select_designer,
        26: create_designers_group,
        27: read_designers_group,
        28: update_designers_group,
        29: delete_designers_group,
        30: select_designers_group,
        31: create_section,
        32: read_section,
        33: update_section,
        34: delete_section,
        35: select_section,
        36: create_template,
        37: read_template,
        38: update_template,
        39: delete_template,
        40: select_template,
        41: create_pattern,
        42: read_pattern,
        43: update_pattern,
        44: delete_pattern,
        45: select_pattern,
        46: create_content,
        47: read_content,
        48: update_content,
        49: delete_content,
        #50: select_content,
        51: create_problem,
        52: read_problem,
        53: update_problem,
        54: delete_problem,
        55: select_problem,
        56: create_i_solution,
        #57: read_i_solution,
        58: update_i_solution,
        59: delete_i_solution,
        60: select_i_solution,
    }




