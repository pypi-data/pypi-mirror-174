import pandas as pd


def ExcelRead(data):
    df = pd.read_excel(data['io'], sheet_name = data['sheet_name'], \
            skiprows=data['skiprows'], skipfooter= data['skipfooter'], \
            index_col=data['index_col'])

    return df

