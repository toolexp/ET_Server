# coding=utf-8

# Import necessary modules
from datetime import datetime
from os import remove

from sqlalchemy import and_

from Modules.Config.base import Session, engine, Base
from Modules.Config.Data import Message
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


def handle_decision(connection):
    Base.metadata.create_all(engine)
    session = Session()
    argument = connection.message.action
    func = switcher_protocol.get(argument, 'nothing')
    return func(connection.message.information, session)


def create_admin(parameters, session):
    """
       Creates an 'Administrator' object and stores it into the DB, the data for the
       object is inside the 'parameters'

       Parameters
       ----------
       parameters: Message.information [string, string, string, string]
           -> parameters[0] has Administrator.name
           -> parameters[1] has Administrator.surname
           -> parameters[2] has Administrator.email
           -> parameters[3] has Administrator.password
       session: Session
           Session of connection with the database

       Returns
       -------
       msg_rspt: Message
           Message with information of the fail or success of the operation

       Raises
       ------
       Exception:
           If any of the lines of code generates an error
       """
    try:
        admin_aux = Administrator(parameters[0], parameters[1], parameters[2], parameters[3])
        session.add(admin_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error creating an administrator: ' + str(e))


def read_admin(parameters, session):
    """
        Retreive a list with al the 'Administrators' registered into the DB. The list
        contains a string representation of each 'Administrator' (__str__())

        Parameters
        ----------
        parameters: Message.information [] (not used)
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with the list of administrators

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        admins = session.query(Administrator).all()
        session.close()
        msg_rspt = Message(action=2, information=[])
        for admin in admins:
            msg_rspt.information.append(admin.__str__())
        return msg_rspt
    except Exception as e:
        raise Exception('Error retrieving administrators: ' + str(e))


def update_admin(parameters, session):
    """
        Update information of an 'Administrator' registered into the DB.

        Parameters
        ----------
        parameters: Message.information [int, string, string, string, string]
           -> parameters[0] has Administrator.id
           -> parameters[1] has Administrator.name
           -> parameters[2] has Administrator.surname
           -> parameters[3] has Administrator.email
           -> parameters[4] has Administrator.password
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the fail or success of the operation

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
        admin_aux.name = parameters[1]
        admin_aux.surname = parameters[2]
        admin_aux.email = parameters[3]
        admin_aux.password = parameters[4]
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error updating administrator: ' + str(e))


def delete_admin(parameters, session):
    """
        Remove an 'Administrator' from the DB.

        Parameters
        ----------
        parameters: Message.information [int]
           -> parameters[0] has Administrator.id
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the fail or success of the operation

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
        session.delete(admin_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error removing administrator: ' + str(e))


def select_admin(parameters, session):
    """
        Retrieve information of an 'Administrator' from the DB.

        Parameters
        ----------
        parameters: Message.information [int]
           -> parameters[0] has Administrator.id
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the 'Administrator'

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        admin_aux = session.query(Administrator).filter(Administrator.id == parameters[0]).first()
        session.close()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(admin_aux.name)
        msg_rspt.information.append(admin_aux.surname)
        msg_rspt.information.append(admin_aux.email)
        msg_rspt.information.append(admin_aux.password)
        return msg_rspt
    except Exception as e:
        raise Exception('Error selecting administrator: ' + str(e))


def create_experimenter(parameters, session):
    """
       Creates an 'Experimenter' object and stores it into the DB, the data for the
       object is inside the 'parameters'

       Parameters
       ----------
       parameters: Message.information [string, string, string, string]
           -> parameters[0] has Experimenter.name
           -> parameters[1] has Experimenter.surname
           -> parameters[2] has Experimenter.email
           -> parameters[3] has Experimenter.password
       session: Session
           Session of connection with the database

       Returns
       -------
       msg_rspt: Message
           Message with information of the fail or success of the operation

       Raises
       ------
       Exception:
           If any of the lines of code generates an error
       """
    try:
        experimenter_aux = Experimenter(parameters[0], parameters[1], parameters[2], parameters[3])
        session.add(experimenter_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error creating experimenter: ' + str(e))


def read_experimenter(parameters, session):
    """
        Retreive a list with al the 'Experimenters' registered into the DB. The list
        contains a string representation of each 'Experimenter' (__str__())

        Parameters
        ----------
        parameters: Message.information [] (not used)
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with the list of experimenters

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        experimenters = session.query(Experimenter).all()
        session.close()
        msg_rspt = Message(action=2, information=[])
        for experimenter in experimenters:
            msg_rspt.information.append(experimenter.__str__())
        return msg_rspt
    except Exception as e:
        raise Exception('Error retrieving experimenters: ' + str(e))


def update_experimenter(parameters, session):
    """
        Update information of an 'Experimenter' registered into the DB.

        Parameters
        ----------
        parameters: Message.information [int, string, string, string, string]
           -> parameters[0] has Experimenter.id
           -> parameters[1] has Experimenter.name
           -> parameters[2] has Experimenter.surname
           -> parameters[3] has Experimenter.email
           -> parameters[4] has Experimenter.password
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the fail or success of the operation

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
        experimenter_aux.name = parameters[1]
        experimenter_aux.surname = parameters[2]
        experimenter_aux.email = parameters[3]
        experimenter_aux.password = parameters[4]
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error updating experimenter: ' + str(e))


def delete_experimenter(parameters, session):
    """
        Remove an 'Experimenter' from the DB.

        Parameters
        ----------
        parameters: Message.information [int]
           -> parameters[0] has Experimenter.id
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the fail or success of the operation

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
        session.delete(experimenter_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error removing experimenter: ' + str(e))


def select_experimenter(parameters, session):
    """
        Retrieve information of an 'Experimenter' from the DB.

        Parameters
        ----------
        parameters: Message.information [int]
           -> parameters[0] has Experimenter.id
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the 'Experimenter'

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        experimenter_aux = session.query(Experimenter).filter(Experimenter.id == parameters[0]).first()
        session.close()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(experimenter_aux.name)
        msg_rspt.information.append(experimenter_aux.surname)
        msg_rspt.information.append(experimenter_aux.email)
        msg_rspt.information.append(experimenter_aux.password)
        return msg_rspt
    except Exception as e:
        raise Exception('Error selecting experimenter: ' + str(e))


def create_designer(parameters, session):
    """
       Creates an 'Designer' object and stores it into the DB, the data for the
       object is inside the 'parameters'

       Parameters
       ----------
       parameters: Message.information [string, string, string, string]
           -> parameters[0] has Designer.name
           -> parameters[1] has Designer.surname
           -> parameters[2] has Designer.email
           -> parameters[3] has Designer.password
       session: Session
           Session of connection with the database

       Returns
       -------
       msg_rspt: Message
           Message with information of the fail or success of the operation

       Raises
       ------
       Exception:
           If any of the lines of code generates an error
       """
    try:
        designer_aux = Designer(parameters[0], parameters[1], parameters[2], parameters[3])
        session.add(designer_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register created successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error creating designer: ' + str(e))


def read_designer(parameters, session):
    """
        Retreive a list with al the 'Designers' registered into the DB. The list
        contains a string representation of each 'Designer' (__str__())

        Parameters
        ----------
        parameters: Message.information [] (not used)
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with the list of experimenters

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        designers = session.query(Designer).all()
        session.close()
        msg_rspt = Message(action=2, information=[])
        for designer in designers:
            msg_rspt.information.append(designer.__str__())
        return msg_rspt
    except Exception as e:
        raise Exception('Error retrieving designers: ' + str(e))


def update_designer(parameters, session):
    """
        Update information of an 'Designer' registered into the DB.

        Parameters
        ----------
        parameters: Message.information [int, string, string, string, string]
           -> parameters[0] has Designer.id
           -> parameters[1] has Designer.name
           -> parameters[2] has Designer.surname
           -> parameters[3] has Designer.email
           -> parameters[4] has Designer.password
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the fail or success of the operation

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
        designer_aux.name = parameters[1]
        designer_aux.surname = parameters[2]
        designer_aux.email = parameters[3]
        designer_aux.password = parameters[4]
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register updated successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error updating designer: ' + str(e))


def delete_designer(parameters, session):
    """
        Remove an 'Designer' from the DB.

        Parameters
        ----------
        parameters: Message.information [int]
           -> parameters[0] has Designer.id
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the fail or success of the operation

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
        session.delete(designer_aux)
        session.commit()
        session.close()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error removing designer: ' + str(e))


def select_designer(parameters, session):
    """
        Retrieve information of an 'Experimenter' from the DB.

        Parameters
        ----------
        parameters: Message.information [int]
           -> parameters[0] has Experimenter.id
        session: Session
            Session of connection with the database

        Returns
        -------
        msg_rspt: Message
            Message with information of the 'Experimenter'

        Raises
        ------
        Exception:
            If any of the lines of code generates an error
        """
    try:
        designer_aux = session.query(Designer).filter(Designer.id == parameters[0]).first()
        session.close()
        msg_rspt = Message(action=2, information=[])
        msg_rspt.information.append(designer_aux.name)
        msg_rspt.information.append(designer_aux.surname)
        msg_rspt.information.append(designer_aux.email)
        msg_rspt.information.append(designer_aux.password)
        return msg_rspt
    except Exception as e:
        raise Exception('Error selecting designer: ' + str(e))


def create_designers_group(parameters, session):
    designers_group_aux = DesignersGroup(parameters[0], parameters[1])
    for item in parameters[2]:
        designer_aux = session.query(Designer).filter(Designer.id == item).first()
        designers_group_aux.designers.append(designer_aux)
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
    for item in parameters[3]:
        designer_aux = session.query(Designer).filter(Designer.id == item).first()
        designers_group_aux.designers.append(designer_aux)
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
    if len(parameters) == 4:
        classification_aux = session.query(Classification).filter(Classification.id == parameters[3]).first()
        section_aux = Section(parameters[0], parameters[1], parameters[2], classification_aux)
    else:
        section_aux = Section(parameters[0], parameters[1], parameters[2])
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
    if len(parameters == 5):
        classification_aux = session.query(Classification).filter(Classification.id == parameters[4]).first()
        section_aux.classification = classification_aux
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_section(parameters, session):
    section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
    try:
        session.delete(section_aux)
        session.commit()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
    except:
        msg_rspt = Message(action=5, comment='Error deleting register')
    finally:
        session.close()
    return msg_rspt


def select_section(parameters, session):
    section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(section_aux.name)
    msg_rspt.information.append(section_aux.description)
    msg_rspt.information.append(section_aux.data_type)
    msg_rspt.information.append(section_aux.classification_id)
    session.close()
    return msg_rspt


def create_template(parameters, session):
    template_aux = Template(parameters[0], parameters[1])
    session.add(template_aux)
    for i in range(0, len(parameters[2])):
        section_aux = session.query(Section).filter(Section.id == parameters[2][i]).first()
        if parameters[3][i] == '✓':
            mandatory = True
        else:
            mandatory = False
        template_sec_aux = TemplateSection(mandatory, i+1, template_aux, section_aux)
        session.add(template_sec_aux)
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
    templates_secs_aux = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]).all()
    for i in range(0, len(templates_secs_aux)):
        session.delete(templates_secs_aux[i])
    for i in range(0,len(parameters[3])):
        section_aux = session.query(Section).filter(Section.id == parameters[3][i]).first()
        if parameters[4][i] == '✓':
            mandatory = True
        else:
            mandatory = False
        template_sec_aux = TemplateSection(mandatory, i+1, template_aux, section_aux)
        session.add(template_sec_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_template(parameters, session):
    template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
    try:
        session.delete(template_aux)
        session.commit()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
    except:
        msg_rspt = Message(action=5, comment='Error deleting register')
    finally:
        session.close()
    return msg_rspt


def select_template(parameters, session):
    # Received --> parameters = [id_template]
    # Return --> msg_rspt = [2, '', [template_name, template_description, [section1._str_(), section2._str_(), ...]]]
    template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(template_aux.name)
    msg_rspt.information.append(template_aux.description)
    msg_rspt.information.append([])
    template_sections_aux = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]).\
        order_by(TemplateSection.position).all()
    for i in range(0, len(template_sections_aux)):
        msg_rspt.information[2].append(template_sections_aux[i].__str__())
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
    # Received --> [id_template]
    # Returned --> [id_pattern (new)]
    template_aux = session.query(Template).filter(Template.id == parameters[0]).first()
    pattern_aux = Pattern(template_aux)
    session.add(pattern_aux)
    session.commit()
    new_pattern_aux = session.query(Pattern).order_by(Pattern.id.desc()).first()
    session.close()
    msg_rspt = Message(action=2, information=[new_pattern_aux.id], comment='Register created successfully')
    return msg_rspt



def read_pattern(parameters, session):
    if len(parameters) == 0:
        patterns = session.query(Pattern).all()
    else:
        # Received --> [id_designer, id_scenario_comp]
        patterns = session.query(Pattern). \
            join(ScenarioComponent.patterns). \
            join(DesignersGroup.designers).filter(and_(Designer.id == parameters[0],
                                                       ScenarioComponent.id == parameters[1])).all()
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
    diagrams_aux = session.query(PatternSection).filter(and_(PatternSection.pattern_id == parameters[0],
                                                             PatternSection.diagram_id != None)).all()
    for item in diagrams_aux:
        delete_diagram([item.diagram_id, 'just remove path'], session)
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
    # Received --> [content, id_pattern, id_temp_section, id_diagram, id_category]
    pattern_aux = session.query(Pattern).filter(Pattern.id == parameters[1]).first()
    template_section_aux = session.query(TemplateSection).filter(TemplateSection.id == parameters[2]).first()
    if parameters[3] is not None:
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[3]).first()
    else:
        diagram_aux = None
    if parameters[4] is not None:
        category_aux = session.query(Category).filter(Category.id == parameters[4]).first()
    else:
        category_aux = None
    content_aux = PatternSection(parameters[0], pattern_aux, template_section_aux, diagram_aux, category_aux)
    session.add(content_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_content(parameters, session):
    if len(parameters) == 0:
        contents = session.query(PatternSection).all()
    elif len(parameters) == 1:
        # Received --> [id_Pattern]
        contents = session.query(PatternSection).filter(PatternSection.pattern_id == parameters[0]).all()
    else:
        # Received --> [id_pattern, id_temp_section]
        contents = session.query(PatternSection).filter(and_(PatternSection.pattern_id == parameters[0],
                                                        PatternSection.temp_section_id == parameters[1])).all()
    msg_rspt = Message(action=2, information=[])
    for item in contents:
        msg_rspt.information.append(item.__str__())
    session.close()
    return msg_rspt


def update_content(parameters, session):
    # Received --> [id_pattern_section, content, id_diagram, id_category]
    content_aux = session.query(PatternSection).filter(PatternSection.id == parameters[0]).first()
    if parameters[2] is not None:
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
    else:
        diagram_aux = None
    if parameters[3] is not None:
        category_aux = session.query(Category).filter(Category.id == parameters[3]).first()
    else:
        category_aux = None
    content_aux.content = parameters[1]
    content_aux.diagram = diagram_aux
    content_aux.category = category_aux
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
    # Neccesary to remove diagram path
    solution_aux = session.query(IdealSolution).filter(IdealSolution.id == problem_aux.ideal_solution_id).first()
    delete_diagram([solution_aux.diagram_id, 'just remove path'], session)
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
    if len(parameters) == 2:
        # Wthout patterns --> parameters=[annotations, id_diagram]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[1]).first()
        i_solution_aux = IdealSolution(parameters[0], diagram_aux)
    else:
        # With patterns--> parameters=[annotations, id_diagram, [id_pattern1, id_pattern2, ...]]
        diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[1]).first()
        i_solution_aux = IdealSolution(parameters[0], diagram_aux)
        i_solution_aux.patterns = []
        for item in parameters[2]:
            pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
            i_solution_aux.patterns.append(pattern_aux)
    session.add(i_solution_aux)
    session.commit()
    new_i_sol_aux = session.query(IdealSolution).order_by(IdealSolution.id.desc()).first()
    session.close()
    msg_rspt = Message(action=2, information=[new_i_sol_aux.id], comment='Register created successfully')
    return msg_rspt


'''def read_i_solution(parameters, session):
    templates = session.query(Template).all()
    msg_rspt = Message(action=2, information=[])
    for template in templates:
        msg_rspt.information.append(template.__str__())
    session.close()
    return msg_rspt'''


def update_i_solution(parameters, session):
    i_solution_aux = session.query(IdealSolution).filter(IdealSolution.id == parameters[0]).first()
    diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[2]).first()
    i_solution_aux.annotations = parameters[1]
    i_solution_aux.diagram = diagram_aux
    i_solution_aux.patterns = []
    if len(parameters) == 4:
        # With patterns--> parameters=[id_i_solution, annotations, id_diagram, [id_pattern1, id_pattern2, ...]]
        for item in parameters[3]:
            pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
            i_solution_aux.patterns.append(pattern_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
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
    msg_rspt.information.append(i_solution_aux.annotations)
    msg_rspt.information.append(i_solution_aux.diagram_id)
    msg_rspt.information.append([])
    for i in range(0, len(i_solution_aux.patterns)):
        msg_rspt.information[2].append(i_solution_aux.patterns[i].__str__())
    session.close()
    return msg_rspt

def create_diagram(parameters, session):
    """
       Creates a 'Diagram' object and stores it into the DB, the data for the
       object is inside the 'parameters'

       Parameters
       ----------
       parameters: Message.information [string, string, string, string]
           -> parameters[0] has Bytes: file content
           -> parameters[1] has string: filename
       session: Session
           Session of connection with the database

       Returns
       -------
       msg_rspt: Message
           Message with information of the fail or success of the operation and the id of the
           created register

       Raises
       ------
       Exception:
           If any of the lines of code generates an error
       """
    try:
        path = './Resources/Diagrams/'
        file = path + datetime.now().strftime("%Y%m%d_%H%M%S") + parameters[1]
        myfile = open(file, 'wb')
        myfile.write(parameters[0])
        myfile.close()
        diagram_aux = Diagram(parameters[1], file)
        session.add(diagram_aux)
        session.commit()
        new_diagram_aux = session.query(Diagram).order_by(Diagram.id.desc()).first()
        session.close()
        msg_rspt = Message(action=2, information=[new_diagram_aux.id], comment='Register created successfully')
        return msg_rspt
    except Exception as e:
        raise Exception('Error creating a diagram: ' + str(e))


def read_diagram(parameters, session):
    templates = session.query(Template).all()
    msg_rspt = Message(action=2, information=[])
    for template in templates:
        msg_rspt.information.append(template.__str__())
    session.close()
    return msg_rspt


def update_diagram(parameters, session):
    # Received --> [id_diagram, file_content, filename]
    diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
    remove(diagram_aux.file_path)
    path = './Resources/Diagrams/'
    file = path + parameters[2]
    myfile = open(file, 'wb')
    myfile.write(parameters[1])
    myfile.close()
    diagram_aux.name = parameters[2]
    diagram_aux.file_path = file
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def delete_diagram(parameters, session):
    diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
    remove(diagram_aux.file_path)
    if len(parameters) == 1:
        session.delete(diagram_aux)
        session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_diagram(parameters, session):
    diagram_aux = session.query(Diagram).filter(Diagram.id == parameters[0]).first()
    myfile = open(diagram_aux.file_path, 'rb')
    file_bytes = myfile.read()
    myfile.close()
    file_name = diagram_aux.name
    session.close()
    msg_rspt = Message(action=2, information=[file_name, file_bytes], comment='Register created successfully')
    return msg_rspt

def create_classification(parameters, session):
    calssification_aux = Classification(parameters[0])
    session.add(calssification_aux)
    session.commit()
    calssification_aux = session.query(Classification).order_by(Classification.id.desc()).first()
    session.close()
    msg_rspt = Message(action=2, information=[calssification_aux.id], comment='Register created successfully')
    return msg_rspt


def read_classification(parameters, session):
    calssifications = session.query(Classification).all()
    msg_rspt = Message(action=2, information=[])
    for item in calssifications:
        msg_rspt.information.append(item.__str__())
    session.close()
    return msg_rspt


def update_classification(parameters, session):
    calssification_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
    calssification_aux.name = parameters[1]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_classification(parameters, session):
    section_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
    try:
        session.delete(section_aux)
        session.commit()
        msg_rspt = Message(action=2, comment='Register deleted successfully')
    except:
        msg_rspt = Message(action=5, comment='Error deleting register')
    finally:
        session.close()
    return msg_rspt


def select_classification(parameters, session):
    classification_aux = session.query(Classification).filter(Classification.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(classification_aux.name)
    msg_rspt.information.append([])
    for item in classification_aux.categories:
        msg_rspt.information[1].append(item.__str__())
    session.close()
    return msg_rspt

def create_category(parameters, session):
    classification_aux = session.query(Classification).filter(Classification.id == parameters[1]).first()
    category_aux = Category(parameters[0], classification_aux)
    session.add(category_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_category(parameters, session):
    if len(parameters) == 0:
        categories = session.query(Category).all()
    else:
        categories = session.query(Category).filter(Category.classification_id == parameters[0]).all()
    msg_rspt = Message(action=2, information=[])
    for item in categories:
        msg_rspt.information.append(item.__str__())
    session.close()
    return msg_rspt


def update_category(parameters, session):
    section_aux = session.query(Section).filter(Section.id == parameters[0]).first()
    section_aux.name = parameters[1]
    section_aux.description = parameters[2]
    section_aux.data_type = parameters[3]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_category(parameters, session):
    # Received --> [id_classification]
    categories_aux = session.query(Category).filter(Category.classification_id == parameters[0]).all()
    for item in categories_aux:
        session.delete(item)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_category(parameters, session):
    category_aux = session.query(Category).filter(Category.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(category_aux.name)
    msg_rspt.information.append(category_aux.classification_id)
    session.close()
    return msg_rspt

def read_template_section(parameters, session):
    if len(parameters) == 0:
        template_sections = session.query(TemplateSection).all()
    else:
        template_sections = session.query(TemplateSection).filter(TemplateSection.template_id == parameters[0]).\
            order_by(TemplateSection.position).all()
    msg_rspt = Message(action=2, information=[])
    for item in template_sections:
        msg_rspt.information.append(item.__str__())
    session.close()
    return msg_rspt

def create_exp_scenario(parameters, session):
    # Received --> [name, description, access_code, start_time, end_time, scenario_availability, scenario_lock, experiment_id, control_group_id, experimental_group_id]
    experiment = session.query(Experiment).filter(Experiment.id == parameters[7]).first()
    control_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[8]).first()
    experimental_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[9]).first()
    exp_sc_aux = ExperimentalScenario(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4],
                                       parameters[5], parameters[6], experiment, control_group, experimental_group)
    session.add(exp_sc_aux)
    session.commit()
    new_exp_sc_aux = session.query(ExperimentalScenario).order_by(ExperimentalScenario.id.desc()).first()
    session.close()
    msg_rspt = Message(action=2, information=[new_exp_sc_aux.id], comment='Register created successfully')
    return msg_rspt


def read_exp_scenario(parameters, session):
    if len(parameters) == 0:
        exp_scenarios = session.query(ExperimentalScenario).all()
    elif len(parameters) == 1:
        # Received --> [id_experiment]
        exp_scenarios = session.query(ExperimentalScenario).filter(ExperimentalScenario.experiment_id == parameters[0]).all()
    else:
        # Received --> [id_designer] (When a designer retrieves available scenarios for him)
        exp_scenarios_ctrl = session.query(ExperimentalScenario).\
            join(ExperimentalScenario.control_group).\
            join(DesignersGroup.designers).filter(and_(Designer.id == parameters[0],
                                                       ExperimentalScenario.scenario_lock == False,
                                                       ExperimentalScenario.scenario_availability == True)).all()
        exp_scenarios_exp = session.query(ExperimentalScenario). \
            join(ExperimentalScenario.experimental_group). \
            join(DesignersGroup.designers).filter(and_(Designer.id == parameters[0],
                                                       ExperimentalScenario.scenario_lock == False,
                                                       ExperimentalScenario.scenario_availability == True)).all()
        exp_scenarios_ctrl += exp_scenarios_exp
        exp_scenarios = exp_scenarios_ctrl
    msg_rspt = Message(action=2, information=[])
    for item in exp_scenarios:
        msg_rspt.information.append(item.__str__())
    session.close()
    return msg_rspt


def update_exp_scenario(parameters, session):
    # Received --> [id_exp_sc, name, description, access_code, start_time, end_time, scenario_availability, scenario_lock, experiment_id, control_group_id, experimental_group_id]
    exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
    experiment = session.query(Experiment).filter(Experiment.id == parameters[8]).first()
    control_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[9]).first()
    experimental_group = session.query(DesignersGroup).filter(DesignersGroup.id == parameters[10]).first()
    exp_sc_aux.name = parameters[1]
    exp_sc_aux.description = parameters[2]
    exp_sc_aux.access_code = parameters[3]
    exp_sc_aux.start_time = parameters[4]
    exp_sc_aux.end_time = parameters[5]
    exp_sc_aux.scenario_availability = parameters[6]
    exp_sc_aux.scenario_lock = parameters[7]
    exp_sc_aux.experiment = experiment
    exp_sc_aux.control_group = control_group
    exp_sc_aux.experimental_group = experimental_group
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_exp_scenario(parameters, session):
    # Received --> [id_exp_scenario]
    exp_scenario_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
    session.delete(exp_scenario_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_exp_scenario(parameters, session):
    # Received --> [id_exp_scenario]
    exp_sc_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(exp_sc_aux.name)
    msg_rspt.information.append(exp_sc_aux.description)
    msg_rspt.information.append(exp_sc_aux.access_code)
    msg_rspt.information.append(exp_sc_aux.start_time)
    msg_rspt.information.append(exp_sc_aux.end_time)
    msg_rspt.information.append(exp_sc_aux.scenario_availability)
    msg_rspt.information.append(exp_sc_aux.scenario_lock)
    msg_rspt.information.append(exp_sc_aux.experiment_id)
    msg_rspt.information.append(exp_sc_aux.control_group_id)
    msg_rspt.information.append(exp_sc_aux.experimental_group_id)
    session.close()
    return msg_rspt

def create_sc_component(parameters, session):
    # Received --> [experimental_scenario_id, problem_id, [cgroup_pattern_id1, cgroup_pattern_id2, ...], [egroup_pattern_id1, egroup_pattern_id2, ...]]
    experimental_scenario_aux = session.query(ExperimentalScenario).filter(ExperimentalScenario.id == parameters[0]).first()
    problem_aux = session.query(Problem).filter(Problem.id == parameters[1]).first()
    sc_component_aux = ScenarioComponent(experimental_scenario_aux, problem_aux)
    session.add(sc_component_aux)
    # Creating association of scenario component and patterns for the control group
    for item in parameters[2]:
        pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
        scc_pattern_aux = ScenarioComponentPattern(1, sc_component_aux, pattern_aux)
        session.add(scc_pattern_aux)
    # Creating association of scenario component and patterns for the experimental group
    for item in parameters[3]:
        pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
        scc_pattern_aux = ScenarioComponentPattern(2, sc_component_aux, pattern_aux)
        session.add(scc_pattern_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_sc_component(parameters, session):
    # Received --> []
    if len(parameters) == 0:
        sc_components = session.query(ScenarioComponent).all()
    else:
        # Received --> [id_exp_scenario, 1]
        # Ask for the scenario components associated with an experimental scenario
        if parameters[1] == 1:
            sc_components = session.query(ScenarioComponent).filter(
                ScenarioComponent.experimental_scenario_id == parameters[0]).all()
        # Received --> [id_sc_component, 2]
        # Ask for the patterns associated with an scenario components
        else:
            sc_components = session.query(ScenarioComponentPattern).filter(
                ScenarioComponentPattern.scenario_component_id == parameters[0]).all()
    msg_rspt = Message(action=2, information=[])
    for item in sc_components:
        msg_rspt.information.append(item.__str__())
    session.close()
    return msg_rspt


def update_sc_component(parameters, session):
    # Received --> [sc_comp_id, problem_id, [cgroup_pattern_id1, cgroup_pattern_id2, ...], [egroup_pattern_id1, egroup_pattern_id2, ...]]
    sc_comp_aux = session.query(ScenarioComponent).filter(ScenarioComponent.id == parameters[0]).first()
    problem_aux = session.query(Problem).filter(Problem.id == parameters[1]).first()
    sc_comp_aux.problem = problem_aux
    # Deleting association of scenario component with pattern
    sc_comp_pat = session.query(ScenarioComponentPattern).\
        filter(ScenarioComponentPattern.scenario_component_id == parameters[0]).all()
    for item in sc_comp_pat:
        session.delete(item)
    # Creating association of scenario component and patterns for the control group
    for item in parameters[2]:
        pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
        scc_pattern_aux = ScenarioComponentPattern(1, sc_comp_aux, pattern_aux)
        session.add(scc_pattern_aux)
    # Creating association of scenario component and patterns for the experimental group
    for item in parameters[3]:
        pattern_aux = session.query(Pattern).filter(Pattern.id == item).first()
        scc_pattern_aux = ScenarioComponentPattern(2, sc_comp_aux, pattern_aux)
        session.add(scc_pattern_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_sc_component(parameters, session):
    # Received --> [id_sc_component]
    sc_comp_aux = session.query(ScenarioComponent).filter(ScenarioComponent.id == parameters[0]).first()
    session.delete(sc_comp_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_sc_component(parameters, session):
    category_aux = session.query(Category).filter(Category.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(category_aux.name)
    msg_rspt.information.append(category_aux.classification_id)
    session.close()
    return msg_rspt

def create_experiment(parameters, session):
    # Received --> [name, description]
    experiment_aux = Experiment(parameters[0], parameters[1])
    session.add(experiment_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register created successfully')
    return msg_rspt


def read_experiment(parameters, session):
    # Received --> []
    experiments = session.query(Experiment).all()
    msg_rspt = Message(action=2, information=[])
    for item in experiments:
        msg_rspt.information.append(item.__str__())
    session.close()
    return msg_rspt


def update_experiment(parameters, session):
    # Received --> [id_experiment, name, description]
    experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
    experiment_aux.name = parameters[1]
    experiment_aux.description = parameters[2]
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register updated successfully')
    return msg_rspt


def delete_experiment(parameters, session):
    # Received --> [id_experiment]
    experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
    session.delete(experiment_aux)
    session.commit()
    session.close()
    msg_rspt = Message(action=2, comment='Register deleted successfully')
    return msg_rspt


def select_experiment(parameters, session):
    experiment_aux = session.query(Experiment).filter(Experiment.id == parameters[0]).first()
    msg_rspt = Message(action=2, information=[])
    msg_rspt.information.append(experiment_aux.name)
    msg_rspt.information.append(experiment_aux.description)
    msg_rspt.information.append([])
    for item in experiment_aux.experimental_scenarios:
        msg_rspt.information[2].append(item.__str__())
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
        61: create_diagram,
        62: read_diagram,
        63: update_diagram,
        64: delete_diagram,
        65: select_diagram,
        66: create_classification,
        67: read_classification,
        68: update_classification,
        69: delete_classification,
        70: select_classification,
        71: create_category,
        72: read_category,
        73: update_category,
        74: delete_category,
        75: select_category,
        #71: create_category,
        77: read_template_section,
        81: create_exp_scenario,
        82: read_exp_scenario,
        83: update_exp_scenario,
        84: delete_exp_scenario,
        85: select_exp_scenario,
        86: create_sc_component,
        87: read_sc_component,
        88: update_sc_component,
        89: delete_sc_component,
        90: select_sc_component,
        91: create_experiment,
        92: read_experiment,
        93: update_experiment,
        94: delete_experiment,
        95: select_experiment
    }




