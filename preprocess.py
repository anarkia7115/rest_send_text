import configparser
import pandas as pd
from pathlib import Path

config = configparser.ConfigParser()
config.read("./config.ini")

def load_clinical_trails(nrows=9999):
    """
    Params:
    Return:
        clinical_trails_df - pd.DataFrame
    """
    clinical_trails_csv = Path(config["PATHS"]["clinical_trails_csv"])
    clinical_trails_df = pd.read_csv(clinical_trails_csv, sep="\t", nrows=nrows, header=0)
    return clinical_trails_df

def keep_text_fileds(df: pd.DataFrame=None):
    """
    Params:
        df - pd.DataFrame:
            clinical_trails_df
    Return:
        df - pd.DataFrame:
            df with only text fields
    """

    column_names_of_text = [
        'condition_or_disease', 
        'detailed_desc', 
        'brief_title', 
        'brief_summary'
    ]
    return df[column_names_of_text]

