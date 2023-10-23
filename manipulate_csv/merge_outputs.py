import glob
import os

import pandas as pd


def combine_intermediate_output(dir_to_combine, well):
    os.chdir(dir_to_combine)
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    path ="D:\\Code_Smile_2.0\\combine_intermedie_output\\"
    if well:
        path = path + "well_engineered\\"
    else:
        path = path + "not_well_engineered\\"
    combined_csv.to_csv(path+"combined_csv.csv", index=False, encoding='utf-8-sig')


def merge_outputs(well):
    combine_intermediate_output("D:\\Code_Smile_2.0\\intermedie_output\\well_engineered_projects\\",well)
    df2 = pd.read_csv('D:\\Code_Smile_2.0\\combined_code_smells\\combined_code_smells.csv')
    if well:
        df1 = pd.read_csv('D:\\Code_Smile_2.0\\combine_intermedie_output\\well_engineered\\combined_csv.csv')
        merged_df_well = df1.merge(df2, left_on=['hash', 'Project_name'], right_on=['tag', 'subject'], how='inner')
        merged_df_well.to_csv('D:\\Code_Smile_2.0\\final_output\\well_engineered'
                              '\\well_engineered_with_code_smells.csv', index=False)

    else:
        df3 = pd.read_csv('D:\\Code_Smile_2.0\\combine_intermedie_output\\not_well_engineered\\combined_csv.csv')
        merged_df_not_well = df3.merge(df2, left_on=['hash', 'Project_name'], right_on=['tag', 'subject'], how='inner')

        merged_df_not_well.to_csv('D:\\Code_Smile_2.0\\final_output\\not_well_engineered'
                                  '\\not_well_engineered_with_code_smells.csv', index=False)
