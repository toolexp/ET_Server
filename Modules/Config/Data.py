from datetime import datetime
import pandas as pd
import shutil
import os
import zipfile
import openpyxl


class Message:

    def __init__(self, action=0, comment='', information=None):
        if information is None:
            information = []
        self.action = action
        self.comment = comment
        self.information = information


def verify_ip(ip):
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
    if not port.isdigit():
        return False
    else:
        return True


def get_experiment_report(experiment=None, session=None):
    from Modules.Classes.ExperimentalScenario import ExperimentalScenario
    from Modules.Classes.Designer import Designer
    from Modules.Classes.Measurement import Measurement
    from Modules.Classes.Metric import Metric
    from Modules.Classes.Problem import Problem
    from Modules.Classes.DesignerExperimentalScenario import DesignerExperimentalScenario
    # Get appropriate name for excel workbook
    words = experiment.name.split(' ')
    for index, word in enumerate(words):
        words[index] = word.lower()
    folder_name = '{}_{}'.format("_".join(words), datetime.now().date().strftime('%Y-%m-%d'))
    os.mkdir('./Resources/{}'.format(folder_name))
    exp_scenarios = session.query(ExperimentalScenario).filter(
        ExperimentalScenario.experiment_id == experiment.id).all()
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
            current_query = session.query(DesignerExperimentalScenario, Designer, Measurement, Metric, Problem). \
                with_entities(Measurement.id.label('measurement_id'), Designer.email.label('user'),
                              DesignerExperimentalScenario.designer_type.label('group_type'),
                              Problem.brief_description.label('problem'), Metric.name.label('metric_type'),
                              Measurement.value.label('measurement'), Measurement.acquisition_start_date,
                              Measurement.acquisition_end_date). \
                join(DesignerExperimentalScenario.designer).join(Designer.measurements).join(Measurement.metric). \
                join(Measurement.problem).filter(Problem.id == problem.id).statement
            current_df = pd.read_sql_query(current_query, session.bind)
            current_sheets.append(current_df)
            current_sheets_names.append(current_sheet_name)
        with pd.ExcelWriter(current_workbook_path + current_workbook_name) as writer:
            for i, current_sheet in enumerate(current_sheets):
                current_sheet.to_excel(writer, sheet_name=current_sheets_names[i])

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
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
