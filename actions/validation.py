import pandas as pd
import pickle
import os

def validation(code):   # called only incase of CAD
    with open('actions/new_data_pickle.pkl','rb') as pickle_file:
        pickle_database_lookup=pd.DataFrame()
        pickle_database_lookup=pickle.load(pickle_file)

    df = pickle_database_lookup.loc[(pickle_database_lookup['Material'] == code) | (pickle_database_lookup['Typkurzbezeichnung'] == code)] # should not matter whether user enter typecode or material number.!    
    if df.empty:
        return ''
    else:
        filter_condition = (df['Material'].apply(str) == code) | (df['Typkurzbezeichnung'] == code)
        material_number = df.loc[filter_condition,"Material"].to_string(index=False)
        type_code= df.loc[filter_condition,"Typkurzbezeichnung"].to_string(index=False)
        return type_code
