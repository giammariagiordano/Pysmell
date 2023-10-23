import shutil

import pandas as pd
import os
import glob


def group_by():
    input = os.path.join("output_smells", "")
    output = os.path.join("..","..","group_smells", "")
    list_csv = ["LargeClass.csv", "LongBaseClassList.csv", "LongMessageChain.csv", "LongMethod.csv",
                "LongParameterList.csv", "LongScopeChaining.csv", "LongTernaryConditionalExpression.csv",
                "MultiplyNestedContainer.csv", "ComplexContainerComprehension.csv", "LongLambdaFunction.csv",
                "ComplexLambdaExpression.csv"]
    for csv in list_csv:
        try:
            path = input + csv
            df = pd.read_csv(path)
            result_df = df.groupby(['subject', 'tag']).size().reset_index(name='Number of Smells')
            result_df['Smell'] = csv.replace(".csv", "")
            result_df.to_csv(output + csv, index=False)
        except Exception as e:

            print("file " + csv + " not found")
            print(output + csv)
            continue


def combine_csv():
    os.chdir(os.path.join("..", "..", "group_smells"))
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv(os.path.join("combined_code_smells", "combined_code_smells.csv"),
                        index=False, encoding='utf-8-sig')


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))
