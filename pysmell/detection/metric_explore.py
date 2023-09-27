import subprocess

import astChecker
import util
import customast
import csv
import numpy as np
import os
from matplotlib import pyplot
from parameter import subject_dir, directory
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

dataset_path = "../../dataset/filtered_no_eng_with_labels.csv"


def open_csv_file(filename):
    return csv.writer(open(os.path.join(metric_directory, filename), 'w'))


def read_dataset(filename=dataset_path):
    df = pd.read_csv( filename)
    df['Project_name'] = df['Project_name'].str.replace('_','/')
    df['Project_name'] = "https://www.github.com/" + df['Project_name'] + ".git"
    return df



def download_github_project(url, save_dir):
    try:
        # Extract the repository name from the URL
        repo_name = url.split("/")[-1]
        # Construct the download URL for a git clone
        git_clone_url = f"git clone {url} {os.path.join(save_dir, repo_name)}"

        # Execute the git clone command
        process = subprocess.Popen(git_clone_url, shell=True)
        process.wait()

        if process.returncode == 0:
            print(f"Downloaded {repo_name}")
        else:
            print(f"Failed to download {repo_name}")

    except Exception as e:
        print(f"Error: {str(e)}")


def download_projects(df):
    github_urls = df['Project_name'].drop_duplicates().to_list()

    save_dir = "downloaded_projects"

    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Use ThreadPoolExecutor to download projects concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        for url in github_urls:
            executor.submit(download_github_project, url, save_dir)


PAR, MLOC, DOC, NBC, CLOC, NOC, LPAR, NOO, TNOC, TNOL, CNOC, NOFF, CNOO, LMC, LEC, DNC, NCT = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []

smells = {'LongParameterList': {'PAR': PAR}, 'LongMethod': {'MLOC': MLOC}, 'LongScopeChaining': {'DOC': DOC},
          'LongBaseClassList': {'NBC': NBC}, 'LargeClass': {'CLOC': CLOC}, 'LongMessageChain': {'LMC': LMC},
          'ComplexLambdaExpression': {'NOC': NOC, 'PAR': LPAR, 'NOO': NOO},
          'LongTernaryConditionalExpression': {'NOC': TNOC, 'NOL': TNOL},
          'ComplexContainerComprehension': {'NOC': CNOC, 'NOFF': NOFF, 'NOO': CNOO},
          'MultiplyNestedContainer': {'LEC': LEC, 'DNC': DNC, 'NCT': NCT}
          }

metric_directory = 'metric'  # Specific directory where you want to store metrics
os.makedirs(metric_directory, exist_ok=True)

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

df = read_dataset()
download_projects(df)
exit(0)

for name in directory.keys():
    sourcedir = os.path.join(subject_dir, name, name)
    tag = directory[name]

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

metric = open(os.path.join(metric_directory, 'metric.txt'), mode='w')

for smellname in smells.keys():
    metric.write("\n####################################%s####################################\n\n" % smellname)
    for metricname in smells[smellname].keys():
        metricdata = smells[smellname][metricname]
        outliers = pyplot.boxplot(metricdata)['fliers'][0].get_data()[1]
        metric.write(
            "%s:  count %d, max %d, min %d, mean %s, plot-box outlier %d-%d, statistic very-high %s, 80th percentile %s\n\n" \
            % (metricname, len(metricdata), max(metricdata), min(metricdata), np.mean(metricdata),
               min(outliers) if len(outliers) > 0 else -1,
               max(outliers) if len(outliers) > 0 else -1, (np.mean(metricdata) + np.std(metricdata)) * 1.5,
               np.percentile(metricdata, 80)))

metric.close()
