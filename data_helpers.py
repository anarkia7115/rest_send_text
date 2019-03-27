"""
Data Helper

"""
import json
import re

import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

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
    bioc_str = \
        "{row_id}.{col_name}|t|\n" +\
        "{row_id}.{col_name}|a|" +\
        row_content.replace("{", "{{").replace("}", "}}") +\
        "\n"
    return bioc_str

def bioc_to_json_records(input_line):
    sep = "\t"
    inner_sep = "."
    if sep not in input_line:
        return None

    var_ner = dict()

    var_ner["ntc_id"] = input_line.split(sep)[0].split(inner_sep)[0]
    var_ner["ner"] = dict()
    var_ner["ner"][input_line.split(sep)[0].split(inner_sep)[1]] = []

    ner_dict = dict()
    ner_dict["start"] = input_line.split(sep)[1]
    ner_dict["end"] = input_line.split(sep)[2]
    ner_dict["text"] = input_line.split(sep)[3]
    ner_dict["label"] = input_line.split(sep)[4]
    ner_dict["normed"] = input_line.split(sep)[5]

    var_ner["ner"][input_line.split(sep)[0].split(inner_sep)[1]].append(ner_dict)

    return var_ner

if __name__ == "__main__":
    pass

