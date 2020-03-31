"""
File with classes and special functions that are required at some point in the project
"""

from datetime import datetime
import pandas as pd
import shutil
import os
import zipfile


class Message:
    """
    A class used to represent the message that is exchanged between server and clients. This message is like the
    communication protocol handled by both endpoints of the communication. A message object has attributes:

    :param action: number that indicates an specific action.
    When message is sent from server to client, possible options for this parameters are:
        - 2: means that the requested action by the client was completed successfully
        - 5: means that the requested action by the client was not completed
        - 6: means that the requested action by the client was completed but with a warning
    When message is sent from client to server, possible options are listed in this project > Modules.Config.protocol
    :type action: int
    :param comment: additional information that may be useful for any of the endpoints
    :type comment: str
    :param information: list of parameters with important information associated with the action of the message
    :type information: list
    """

    def __init__(self, action=0, comment='', information=None):
        """
        Constructor of the class
        """
        if information is None:
            information = []
        self.action = action
        self.comment = comment
        self.information = information


def verify_ip(ip):
    """
    Verifies that the format of an IP address is correct

    :param ip: ip address
    :type ip: str
    :return: success or not depending on the validation
    :rtype: bool
    """
    try:
        digits = ip.split('.')
        for item in digits:
            if not item.isdigit():
                return False
            if int(item) > 255:
                return False
    except:
        return False
    return True


def verify_port(port):
    """
    Verifies that the format of a port number is correct (number and range)

    :param port: port number
    :type port: str
    :return: success or not depending on the validation
    :rtype: bool
    """
    if port.isdigit():
        if 1023 < int(port) <= 65535:
            return True
    return False


def get_experiment_report(experiment=None, session=None):
    """
    Creates a zipped report with all detailed information of a finished experiment. Stores the created zipped file
    into Resources.Reports folder and returns the path of the file so it can be stored in the database.

    :param experiment: experiment object queried from the database from which the report will be created
    :type experiment: Modules.Classes.Experiment.Experiment
    :param session: session established with the database
    :type session: Modules.Config.base.Session
    :return: newly created experiment report path
    :rtype: str
    :return: newly created experiment filename
    :rtype: str
    """
    from Modules.Classes.ExperimentalScenario import ExperimentalScenario
    from Modules.Classes.Designer import Designer
    from Modules.Classes.Measurement import Measurement
    from Modules.Classes.Metric import Metric
    from Modules.Classes.Problem import Problem
    # Get appropriate name for excel workbook
    words = experiment.name.split(' ')
    for index, word in enumerate(words):
        words[index] = word.lower()
    folder_name = '{}_{}'.format("_".join(words), datetime.now().date().strftime('%Y-%m-%d'))
    os.mkdir('./Resources/{}'.format(folder_name))
    exp_scenarios = session.query(ExperimentalScenario).filter(
        ExperimentalScenario.experiment_id == experiment.id).order_by(ExperimentalScenario.title).all()
    # Get scenarios of experiment (each scenario is an excel workbook)
    for counter_sc, scenario in enumerate(exp_scenarios):
        # Get appropriate name for excel workbook
        words = scenario.title.split(' ')
        for index, word in enumerate(words):
            words[index] = word.lower()
        current_workbook_name = 'sc{}_{}.xlsx'.format(counter_sc + 1, "_".join(words))
        current_workbook_path = './Resources/{}/'.format(folder_name)
        # Get problems of current scenario (each problem is a workbook sheet)
        current_sheets = []
        current_sheets_names = []
        for counter_p, problem in enumerate(scenario.problems):
            # Get appropriate name for excel sheet
            words = problem.brief_description.split(' ')
            for index, word in enumerate(words):
                words[index] = word.lower()
            # Get dataframe of measurements of current problem
            current_sheet_name = 'p{}_{}'.format(counter_p + 1, "_".join(words))
            current_query = session.query(Problem, Measurement, Designer, Metric). \
                with_entities(Measurement.id.label('measurement_id'), Designer.email.label('designer'),
                              Problem.brief_description.label('problem'), Metric.name.label('metric_type'),
                              Measurement.value.label('measurement_value'), Measurement.acquisition_start_date,
                              Measurement.acquisition_end_date). \
                join(Problem.measurements).join(Measurement.designer).join(Measurement.metric). \
                filter(Problem.id == problem.id).order_by(Designer.email).statement
            current_df = pd.read_sql_query(current_query, session.bind)
            current_df.loc[current_df['measurement_value'] == -1, 'measurement_value'] = 'Did not execute'
            current_df.loc[current_df['measurement_value'] == -2, 'measurement_value'] = 'Exited unexpectedly'
            current_sheets.append(current_df)
            current_sheets_names.append(current_sheet_name)
        with pd.ExcelWriter(current_workbook_path + current_workbook_name) as writer:
            for i, current_sheet in enumerate(current_sheets):
                current_sheet.to_excel(writer, sheet_name=current_sheets_names[i], index=False)

    # Zip folder with all workbooks in it
    report_path = './Resources/Reports/'
    report_filename = '{}.zip'.format(folder_name)
    zipf = zipfile.ZipFile(report_path + report_filename, 'w', zipfile.ZIP_DEFLATED)
    zipdir('./Resources/{}/'.format(folder_name), zipf)
    zipf.close()

    # Remove temporal files
    shutil.rmtree('./Resources/{}/'.format(folder_name))

    # Return info to be saved into database
    return report_filename, report_path + report_filename


def zipdir(path, ziph):
    """
    Zips a folder with all its content.

    :param path: path of current folder that wants to be zipped
    :type path: str
    :param ziph: zipfile object where de folder will be zipped
    :type ziph: zipfile.ZipFile
    """
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
