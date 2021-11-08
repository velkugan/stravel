import pandas as pd

df = pd.read_csv("Python Scripts/Top_10000_Popular_Movies.csv")


# return actual data type of columns from Data Frame
def true_data_type(data_frame):
    return {col: data_frame[col].apply(lambda x: type(x)).unique().tolist() for col in df.columns}


def string_validation(data_frame, data_column):
    col_dup = data_frame[data_column].duplicated()
    return col_dup


true_types = true_data_type(df)
for col in df:
    # print(true_types[col] == [str])
    if true_types[col] == [str]:
        print(string_validation(df, col))
    # print(col)
