import pandas as pd
import os


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
            result = df.groupby(["subject", "tag"]).count().reset_index()
            result['Smell'] = csv.replace(".csv","")
            result.to_csv(output + csv, index=False)
        except Exception as e:
            print("file " + csv + " not found")
            print(basedir+csv)
            continue
