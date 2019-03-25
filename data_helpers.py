"""
Data Helper

"""
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

import json
def dict_save(row_generator, output_file):
    with open(output_file, 'w') as fw:
        for row in row_generator:
            row_json = json.dumps(row)
            fw.write(row_json+"\n")

def dict_load(json_records_file):
    with open(json_records_file) as f_in:
        for row in f_in:
            row_json = json.loads(row)
            yield row_json

def map_dict_value(row, key_column_name, map_func):
    mapped_row = dict()
    for col_name, col_val in row.items():
        if col_name == key_column_name:  # is a key to identify row
            row_key = col_val
        else:  # is text, predict
            mapped_val = map_func(col_val)  
            mapped_row[col_name] = mapped_val

        assert row_key is not None

        return row_key, mapped_row

def json_record_to_bioc(row_content):
    bioc_str = (
        "{row_id}.{col_name}|t|\n"
        "{row_id}.{col_name}|a|{row_content}\n"
    
    ).format(row_content=row_content)
    return bioc_str

def json_records_to_bioc():
    """
    dict rows to bioc format, for tmVar
    """
    json_records_file = config["PATHS"]["json_records"]
    bioc_file = config["PATHS"]["bioc"]
    key_column_name = "nct_id"
    row_dict_generator = dict_load(json_records_file)

    f_bioc = open(bioc_file, 'w')
    for row_dict in row_dict_generator:
        row_key, bioc_by_colname= map_dict_value(
            row_dict, key_column_name, json_record_to_bioc)
        for col_name, bioc in bioc_by_colname.items():
            bioc = bioc.format(row_id=row_key, col_name=col_name)
            f_bioc.write(bioc + "\n")
    f_bioc.close()

if __name__ == "__main__":
    json_records_to_bioc()
