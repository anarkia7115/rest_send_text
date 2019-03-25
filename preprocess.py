import configparser
import pandas as pd
from pathlib import Path
import os


config = configparser.ConfigParser()
config.read("./config.ini")

def load_text_to_dist(file_path, num_rows, sep="\t"):
    row_counter = 0
    with open(file_path, encoding="utf8", mode='r') as records:
        header = records.readline().strip()
        header = header.split("\t")
        for record in records:
            record = record.strip().split("\t")
            if num_rows is None or row_counter < num_rows:
                yield dict(zip(header, record))
                row_counter += 1
            else:
                break

def load_clinical_trails(nrows=9999, return_type='df', sep="\t"):
    """
    Params:
    Return:
        clinical_trails_df - pd.DataFrame
    """
    clinical_trails_csv = Path(config["PATHS"]["clinical_trails_csv"])
    if return_type == 'df':
        clinical_trails_df = pd.read_csv(clinical_trails_csv, sep=sep, nrows=nrows, header=0, encoding='utf8')
        return clinical_trails_df
    elif return_type == 'dict':
        return load_text_to_dist(clinical_trails_csv, num_rows=nrows, sep=sep)

def keep_text_fileds(rows):
    """
    Params:
        df - pd.DataFrame:
            clinical_trails_df
    Return:
        df - pd.DataFrame:
            df with only text fields
    """

    column_names_of_text = [
        'nct_id', 
        'condition_or_disease', 
        'detailed_desc', 
        'brief_title', 
        'brief_summary'
    ]
    import types
    if isinstance(rows, pd.DataFrame):

        for row in rows[column_names_of_text].to_dict(orient='records'):
            yield row
    elif isinstance(rows, types.GeneratorType):
        column_names_of_text = set(column_names_of_text)
        for row in rows:
            new_row = dict()
            for k, v in row.items():
                if k in column_names_of_text:
                    new_row[k] = v
            yield new_row
    else:
        raise Exception("unknown type of data")

def load_clinical_trails_text(nrows, returntype, sep='\t'):
    row_records_file = config["PATHS"]["row_records"]
    if os.path.isfile(row_records_file):
        import data_helpers
        return data_helpers.dict_load(row_records_file)
    else:
        ct = load_clinical_trails(
            nrows=nrows, 
            return_type=returntype, 
            sep=sep
        )
        ct_text = keep_text_fileds(ct)
        return ct_text