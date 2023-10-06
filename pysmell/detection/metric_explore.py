import subprocess
import astChecker
import util
import customast
import csv
import numpy as np
import os
from matplotlib import pyplot
import pandas as pd
import logging

from manipulate_csv.add_labels import add_labels_df
from manipulate_csv.get_information_from_initial_dataset import read_csv, set_logging, split_dataset, download_projects, \
    build_dataset_with_pyDriller
from manipulate_csv.merge_outputs import merge_outputs
from manipulate_csv.post_analysis import group_by, combine_csv

metric_directory = 'metric'
os.makedirs(metric_directory, exist_ok=True)

dataset_path = "../../dataset/filtered_no_eng_with_labels.csv"

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_list_sha_from_project(df, name):
    filtered_df = df[df.apply(lambda row: name in row['Project_name'], axis=1)]
    return filtered_df['Commit_Hash'].drop_duplicates().to_list()


def get_list_projects(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return dirs


def open_csv_file(filename):
    return csv.writer(open(os.path.join(metric_directory, filename), 'w'))


def checkout(path, project, sha):
    try:
        project_path = os.path.join(path, project)
        git_checkout = f"git checkout {sha}"
        process = subprocess.Popen(git_checkout, shell=True, cwd=project_path)
        process.wait()
        if process.returncode == 0:
            print(f"Checked out {project} at {sha}")
            logging.info(f"Checked out {project} at {sha}")
        else:
            print(f"Failed to checkout {project} at {sha}")
            logging.error(f"Failed to checkout {project} at {sha}")
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Error: {str(e)}")


# if is_engineered true, then the dataset is the one with the engineered projects
def run_py_smell(df, is_engineered):
    download_projects_path = "../../projects"
    PAR, MLOC, DOC, NBC, CLOC, NOC, LPAR, NOO, TNOC, TNOL, CNOC, NOFF, CNOO, LMC, LEC, DNC, NCT = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

    smells = {'LongParameterList': {'PAR': PAR}, 'LongMethod': {'MLOC': MLOC}, 'LongScopeChaining': {'DOC': DOC},
              'LongBaseClassList': {'NBC': NBC}, 'LargeClass': {'CLOC': CLOC}, 'LongMessageChain': {'LMC': LMC},
              'ComplexLambdaExpression': {'NOC': NOC, 'PAR': LPAR, 'NOO': NOO},
              'LongTernaryConditionalExpression': {'NOC': TNOC, 'NOL': TNOL},
              'ComplexContainerComprehension': {'NOC': CNOC, 'NOFF': NOFF, 'NOO': CNOO},
              'MultiplyNestedContainer': {'LEC': LEC, 'DNC': DNC, 'NCT': NCT}
              }

    LongParameter = open_csv_file('LongParameterList.csv')
    LongParameter.writerow(['subject', 'tag', 'file', 'lineno', 'PAR'])
    LongMethod = open_csv_file('LongMethod.csv')
    LongMethod.writerow(['subject', 'tag', 'file', 'lineno', 'MLOC'])
    LongScopeChaining = open_csv_file('LongScopeChaining.csv')
    LongScopeChaining.writerow(['subject', 'tag', 'file', 'lineno', 'DOC'])
    LongBaseClass = open_csv_file('LongBaseClassList.csv')
    LongBaseClass.writerow(['subject', 'tag', 'file', 'lineno', 'NBC'])
    LargeClass = open_csv_file('LargeClass.csv')
    LargeClass.writerow(['subject', 'tag', 'file', 'lineno', 'CLOC'])
    ComplexLambda = open_csv_file('ComplexLambdaExpression.csv')
    ComplexLambda.writerow(['subject', 'tag', 'file', 'lineno', 'NOC', 'PAR', 'NOO'])
    LongTernary = open_csv_file('LongTernaryConditionalExpression.csv')
    LongTernary.writerow(['subject', 'tag', 'file', 'lineno', 'NOC', 'NOL'])
    ContainerComprehension = open_csv_file('ComplexContainerComprehension.csv')
    ContainerComprehension.writerow(['subject', 'tag', 'file', 'lineno', 'NOC', 'NOFF', 'NOO'])
    LongMessageChain = open_csv_file('LongMessageChain.csv')
    LongMessageChain.writerow(['subject', 'tag', 'file', 'lineno', 'LMC'])
    MultiplyNestedContainer = open_csv_file('MultiplyNestedContainer.csv')
    MultiplyNestedContainer.writerow(['subject', 'tag', 'file', 'lineno', 'LEC', 'DNC', 'NCT'])
    if is_engineered:
        download_projects_path_complete = download_projects_path + '/well_engineered_projects/'
    else:
        download_projects_path_complete = download_projects_path + '/not_well_engineered_projects/'

    for row in df.iterrows():
        try:
            name = row[1]['Project_name']
            sha = row[1]['hash']
            print("analyzing commit: ", sha)
            checkout(download_projects_path_complete, name, sha)
            sourcedir = download_projects_path_complete + name
            tag = sha
            for currentFileName in util.walkDirectory(sourcedir):
                try:
                    astContent = customast.parse_file(currentFileName)
                except Exception as e:
                    print(name, tag, currentFileName)
                    continue
                myast = astChecker.MyAst()
                myast.fileName = currentFileName
                myast.visit(astContent)
                for item in myast.result:
                    if item[0] == 1:
                        PAR.append(item[3])
                        LongParameter.writerow([name, tag, item[1], item[2], item[3]])
                    elif item[0] == 2:
                        MLOC.append(item[3])
                        LongMethod.writerow([name, tag, item[1], item[2], item[3]])
                    elif item[0] == 3:
                        DOC.append(item[3])
                        LongScopeChaining.writerow([name, tag, item[1], item[2], item[3]])
                    elif item[0] == 4:
                        NBC.append(item[3])
                        LongBaseClass.writerow([name, tag, item[1], item[2], item[3]])
                    elif item[0] == 5:
                        CLOC.append(item[3])
                        LargeClass.writerow([name, tag, item[1], item[2], item[3]])
                    elif item[0] == 6:
                        if len(item) == 4:
                            LEC.append(item[3])
                            MultiplyNestedContainer.writerow([name, tag, item[1], item[2], item[3], '', ''])
                        else:
                            DNC.append(item[3])
                            NCT.append(item[4])
                            MultiplyNestedContainer.writerow([name, tag, item[1], item[2], '', item[3], item[4]])
                    elif item[0] == 9:
                        NOC.append(item[3])
                        LPAR.append(item[4])
                        NOO.append(item[5])
                        ComplexLambda.writerow([name, tag, item[1], item[2], item[3], item[4], item[5]])
                    elif item[0] == 10:
                        TNOC.append(item[3])
                        TNOL.append(item[4])
                        LongTernary.writerow([name, tag, item[1], item[2], item[3], item[4]])
                    elif item[0] == 11:
                        CNOC.append(item[3])
                        NOFF.append(item[4])
                        CNOO.append(item[5])
                        ContainerComprehension.writerow([name, tag, item[1], item[2], item[3], item[4], item[5]])
                    elif item[0] == 13:
                        LMC.append(item[3])
                        LongMessageChain.writerow([name, tag, item[1], item[2], item[3]])
        except Exception as e:
            print(e)
            print(metric_directory + "metric.txt")
            continue

    metric = open(os.path.join(metric_directory, 'metric.txt'), mode='w')
    for smellname in smells.keys():
        metric.write(
            "\n####################################" + smellname + "####" + name + "################################\n\n")
        for metricname in smells[smellname].keys():
            metricdata = smells[smellname][metricname]
            outliers = pyplot.boxplot(metricdata)['fliers'][0].get_data()[1]
            if metricdata != []:
                print(metricname, len(metricdata), max(metricdata), min(metricdata), np.mean(metricdata),
                        min(outliers) if len(outliers) > 0 else -1)
                metric.write(
                        "%s:  count %d, max %d, min %d, mean %s, plot-box outlier %d-%d, statistic very-high %s, 80th percentile %s\n\n" \
                    % (metricname, len(metricdata), max(metricdata), min(metricdata), np.mean(metricdata),
                        min(outliers) if len(outliers) > 0 else -1,
                        max(outliers) if len(outliers) > 0 else -1, (np.mean(metricdata) + np.std(metricdata)) * 1.5,
                        np.percentile(metricdata, 80)))
    metric.close()

    files = ['LongParameterList.csv', 'LongMethod.csv', 'LongScopeChaining.csv', 'LongBaseClassList.csv',
             'LargeClass.csv',
             'ComplexLambdaExpression.csv', 'LongTernaryConditionalExpression.csv', 'ComplexContainerComprehension.csv',
             'LongMessageChain.csv', 'MultiplyNestedContainer.csv']

    for file in files:
        try:
            print('metric/' + file)
            df = pd.read_csv("metric/" + file)
            df = df.drop_duplicates()
            df.to_csv("metric/" + file, index=False)
        except:
            continue


def main():
    path = "../../dataset/NICHE.csv"
    set_logging()
    df = read_csv(path)
    df_y_Engineered, df_n_Engineered = split_dataset(df)
    df_y_Engineered.to_csv('../../dataset/NICHE_y_Engineered.csv', index=False)
    df_n_Engineered.to_csv('../../dataset/NICHE_n_Engineered.csv', index=False)
    download_projects(df_y_Engineered, "well_engineered_projects")
    download_projects(df_n_Engineered, "not_well_engineered_projects")
    df_y_Engineered = build_dataset_with_pyDriller(True)
    df_n_Engineered = build_dataset_with_pyDriller(False)
    df_y_Engineered = add_labels_df(df_y_Engineered)
    df_n_Engineered = add_labels_df(df_n_Engineered)

    df_y_Engineered.to_csv('../../dataset/NICHE_y_Engineered_pyDriller.csv', index=False)
    df_n_Engineered.to_csv('../../dataset/NICHE_n_Engineered_pyDriller.csv', index=False)
    run_py_smell(df_y_Engineered,True)
    run_py_smell(df_n_Engineered,False)
    group_by()
    combine_csv()
    merge_outputs()


if __name__ == "__main__":
    main()
