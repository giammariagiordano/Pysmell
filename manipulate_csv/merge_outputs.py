import pandas as pd


def merge_outputs():
    df1 = pd.read_csv('/Users/broke31/Desktop/Pysmell/dataset/NICHE_y_Engineered_pyDriller.csv')
    df2 = pd.read_csv('/Users/broke31/Desktop/Pysmell/combined_code_smells/combined_code_smells.csv')
    df3 = pd.read_csv('/Users/broke31/Desktop/Pysmell/dataset/NICHE_n_Engineered_pyDriller.csv')
    merged_df_well = df1.merge(df2, left_on=['hash', 'Project_name'], right_on=['tag', 'subject'], how='inner')
    merged_df_not_well = df3.merge(df2, left_on=['hash', 'Project_name'], right_on=['tag', 'subject'], how='inner')
    merged_df_well.to_csv('/Users/broke31/Desktop/Pysmell/final_output/well_engineered/well_engineered_with_code_smells.csv', index=False)
    merged_df_not_well.to_csv('/Users/broke31/Desktop/Pysmell/final_output/not_well_engineered/not_well_engineered_with_code_smells.csv', index=False)