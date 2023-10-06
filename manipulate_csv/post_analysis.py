import pandas as pd
import os
import glob

def group_by():
    basedir = "/Users/broke31/Desktop/Pysmell/pysmell/detection/metric/"
    output = "/Users/broke31/Desktop/Pysmell/output_smells/"

    list_csv = ["LargeClass.csv", "LongBaseClassList.csv", "LongMessageChain.csv", "LongMethod.csv",
                "LongParameterList.csv", "LongScopeChaining.csv", "LongTernaryConditionalExpression.csv",
                "MultiplyNestedContainer.csv", "ComplexContainerComprehension.csv", "LongLambdaFunction.csv",
                "ComplexLambdaExpression.csv"]
    for csv in list_csv:
        try:
            path = basedir+csv
            df = pd.read_csv(path)
            result_df = df.groupby(['subject', 'tag']).size().reset_index(name='Number of Smells')
            result_df['Smell'] = csv.replace(".csv", "")
            result_df.to_csv(output + csv, index=False)
        except Exception as e:
            print("file " + csv + " not found")
            print(basedir+csv)
            continue


def combine_csv():
    os.chdir("/Users/broke31/Desktop/Pysmell/output_smells/")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("/Users/broke31/Desktop/Pysmell/combined_code_smells/combined_code_smells.csv",
                        index=False, encoding='utf-8-sig')

