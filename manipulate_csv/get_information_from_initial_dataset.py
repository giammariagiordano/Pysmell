import os
import subprocess

import pandas as pd
import logging
from concurrent.futures import ThreadPoolExecutor

from pydriller import Repository


def read_csv(path):
    df = pd.read_csv(path)
    df['Project_name'] = df['GitHub Repo'].str.replace('_', '/')
    df['Project_name'] = "https://www.github.com/" + df['Project_name'] + ".git"
    return df


def set_logging():
    logging.basicConfig(filename='log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def split_dataset(df):
    df_y_Engineered = df[df['Engineered ML Project'] == 'Y']
    df_n_Engineered = df[df['Engineered ML Project'] == 'N']
    return df_y_Engineered, df_n_Engineered


def download_github_project(url, save_dir):
    try:
        repo_name = url.split("/")[-1]
        git_clone_url = f"git clone {url} {os.path.join(save_dir, repo_name.replace('.git', ''))}"
        process = subprocess.Popen(git_clone_url, shell=True)
        process.wait()
        if process.returncode == 0:
            print(f"Downloaded {repo_name}")
            logging.info(f"Downloaded {repo_name}")
            #os.replace(os.path.join(save_dir, repo_name), os.path.join(save_dir, repo_name).replace(".git", ""))
        else:
            print(f"Failed to download {repo_name}")
            logging.error(f"Failed to download {repo_name}")

    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Error: {str(e)}")


def download_projects(df, name_dir):
    try:
        github_urls = df['Project_name'].drop_duplicates().to_list()
        save_dir = "../../projects/" + name_dir + "/"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        with ThreadPoolExecutor(max_workers=4) as executor:
            for url in github_urls:
                executor.submit(download_github_project, url, save_dir)
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Error: {str(e)}")



def get_list_of_projects_from_dir(is_engineered):
    list_of_projects = []
    if is_engineered:
        well = "well_engineered_projects"
    else:
        well = "not_well_engineered_projects"

    well_path = "../../projects/" + well

    if os.path.exists(well_path):
        for dir_name in os.listdir(well_path):
            dir_path = os.path.join(well_path, dir_name)
            if os.path.isdir(dir_path):
                list_of_projects.append(dir_path)


    return list_of_projects


def build_dataset_with_pyDriller(is_engineered):
    project_list = get_list_of_projects_from_dir(is_engineered)
    data_list = []
    for project in project_list:
        print(f"Recupero delle informazioni sulla commit per il progetto: {project}")
        for commit in Repository(project).traverse_commits():
            commit_info = {
                'hash': commit.hash,
                'msg': commit.msg,
                'deletions': commit.deletions,
                'files': commit.files,
                'date': commit.author_date,
                'Path': project,
                'Project_name': project.split("/")[-1].replace(".git", "")
            }
            data_list.append(commit_info)

    to_return = pd.DataFrame(data_list)
    return to_return
