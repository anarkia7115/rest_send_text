import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

def ner_result_format(ner_result):
    """
    Params:
        ner_result - dict, having keys {'ents', 'text', 'title'}
            |- ents
                |- start: int
                |- end: int
                |- label (DISO, PRGE, CHED)
                |- text
    Returns:
        list of dict:
            |- start: int
            |- end: int
            |- label (DISO, PRGE, CHED)
            |- text
    """
    if ner_result is None:
        return None
    else:
        return ner_result['ents']

def save_dict_rows():
    output_file = config["PATHS"]["json_records"]
    import preprocess
    dict_rows = preprocess.load_clinical_trails_text(None, 'dict')
    import data_helpers
    data_helpers.dict_save(dict_rows, output_file)

def json_records_to_bioc():
    """
    dict rows to bioc format, for tmVar
    """
    from data_helpers import dict_load, map_dict_value, json_record_to_bioc

    json_records_file = config["PATHS"]["json_records"]
    bioc_file = config["PATHS"]["bioc"]
    key_column_name = "nct_id"
    row_dict_generator = dict_load(json_records_file)

    f_bioc = open(bioc_file, 'w')
    for row_dict in row_dict_generator:
        print("getting row")
        row_key, bioc_by_colname= map_dict_value(
            row_dict, key_column_name, json_record_to_bioc)
        for col_name, bioc in bioc_by_colname.items():
            print("getting item")
            try:
                bioc = bioc.format(
                    row_id=row_key, col_name=col_name)
            except IndexError:
                print("bioc:{}\nrow_id:{}\ncol_name:{}\n".format(
                    bioc, row_key, col_name))
                raise
            f_bioc.write(bioc + "\n")
    f_bioc.close()

def write_bioc_to_json_records():
    from data_helpers import bioc_to_json_records
    import json

    tmvar_bioc_path = config["PATHS"]["tmvar_bioc"]
    tmvar_json = config["PATHS"]["tmvar_json"]
    with open(tmvar_bioc_path, encoding='utf8') as f_in, \
        open(tmvar_json, 'w') as f_w:
        for content in f_in:
            ner_json = bioc_to_json_records(content.strip())
            if ner_json is not None:
                f_w.write(json.dumps(ner_json) + "\n")

if __name__ == "__main__":
    write_bioc_to_json_records()