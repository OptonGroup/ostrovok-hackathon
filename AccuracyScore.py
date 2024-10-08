import pandas as pd
from sklearn.metrics import accuracy_score

def compare_csv_files(file1, file2):
    df1 = pd.read_csv(file1, encoding='latin-1')
    df1.fillna('undefined', inplace=True)
    df2 = pd.read_csv(file2, encoding='utf-16')
    df2.fillna('undefined', inplace=True)
    
    common_columns = df1.columns.intersection(df2.columns)
    
    # Filter both dataframes by the common columns
    df1_common = df1[common_columns]
    df2_common = df2[common_columns]
    
    if len(df1_common) < len(df2_common):
        df2_common = df2_common.iloc[:len(df1_common)]
    elif len(df2_common) < len(df1_common):
        df1_common = df1_common.iloc[:len(df2_common)]
    
    corr = 0
    for i in range(len(df1_common)):
        if df1_common.iloc[i].equals(df2_common.iloc[i]):
            corr += 1

    accuracy = (corr / len(df1_common)) * 100
    
    return accuracy