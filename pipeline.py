import preprocess
import postprocess
import configparser
import compute
import json
from multiprocessing.pool import Pool

config = configparser.ConfigParser()
config.read("./config.ini")


def compute_ner_from_file_input(input_file, nrows, key_column_name, predictor=compute.get_ner):
    """
    Params:
        predictor - ner = predictor(input_text)

    1. load text
    2. process every list, predict ner
    3. yield prediction value
    """
    ct_text_rows = preprocess.load_clinical_trails_text(nrows=nrows, returntype='dict')

    num_of_rows = 0

    for row in ct_text_rows:
        row_key = None
        predicted_ners = dict()
        for col_name, col_val in row.items():
            if col_name == key_column_name:  # is a key to identify row
                row_key = col_val
            else:  # is text, predict
                ner_result = predictor(col_val)  # predict
                ner_result = postprocess.ner_result_format(ner_result)  # format
                predicted_ners[col_name] = ner_result
        assert row_key is not None
        num_of_rows += 1
        print("{} rows processed".format(num_of_rows))
        yield {
            key_column_name: row_key, 
            "ner": predicted_ners
        }

def save_clinical_trails_ner_to_file(nrows=999):
    ner_json_path = config["PATHS"]["ner_json"]
    input_file = config["PATHS"]["clinical_trails_csv"]

    key_column_name = 'nct_id'
    ner_result_generator = compute_ner_from_file_input(
        input_file=input_file, 
        nrows=nrows, 
        key_column_name=key_column_name
    )

    with open(ner_json_path, 'w') as f_json_output:
        for ner_result in ner_result_generator:
            f_json_output.write(json.dumps(ner_result) + "\n")


def save_clinical_trails_ner_to_file_multi_process(nrows=999):
    ner_json_path = config["PATHS"]["ner_json"]
    input_file = config["PATHS"]["clinical_trails_csv"]

    key_column_name = 'nct_id'
    ner_result_generator = compute_ner_from_file_input(
        input_file=input_file, 
        nrows=nrows, 
        key_column_name=key_column_name
    )

    p = Pool(6)

    with open(ner_json_path, 'w') as f_json_output:

        for ner_result in p.map(next, ner_result_generator):
            f_json_output.write(json.dumps(ner_result) + "\n")

if __name__ == "__main__":
    # save_clinical_trails_ner_to_file()
    save_clinical_trails_ner_to_file_multi_process()