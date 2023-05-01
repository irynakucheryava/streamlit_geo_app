import pandas as pd


def data_count(data, col, col_name):
    '''
    Functions returns data with count per category
    from the main dataset

    Parameters
    ----------
    data : pd.DataFrame
        Main dataset
    col : str
        A string of the columns to select.
    col_name : str
        A new column name

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''
    df = data.loc[:,data.columns.str.startswith(col)].sum().reset_index()
    df.columns = [col_name, 'Count']
    df[col_name] = df[col_name].str.replace(col + '_', '')

    return df
