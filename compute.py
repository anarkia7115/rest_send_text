import configparser
import time
import requests, json
import postprocess
from multiprocessing import Queue


config = configparser.ConfigParser()
config.read("./config.ini")

def get_ner(text, port=config["SABER"]["port"]):
    """
    Args:
        text - string

    Return:
        ner - dict
    """
    start_time = time.time()

    # importing the requests library 
    
    # api-endpoint 
    URL = "http://{host}:{port}/annotate/text".format(
        host=config["SABER"]["host"],
        port=port
    )
    
    # defining a params dict for the parameters to be sent to the API 
    input_data = {'text':text} 

    headers = {'content-type': 'application/json'}
    
    r = requests.post(url=URL, data=json.dumps(input_data), headers=headers) 
    # r.status_code
    ner_result = r.json() 
    
    print("--- %s seconds in ner ---" % (time.time() - start_time))
    return ner_result

def process_clinical_trails_row(
    row, 
    key_column_name, 
    predictor, 
    some_q:Queue=None):
    """
    Params:
        row - clinical trails row
        key_column_name - column_name of key
        predictor - predictor function: ner = predictor(input_text)

    Return:
        row_key - the key of row (None empty)
        predicted_ners - analyzed row

    """
    predicted_ners = dict()
    for col_name, col_val in row.items():
        if col_name == key_column_name:  # is a key to identify row
            row_key = col_val
        else:  # is text, predict
            ner_result = predictor(col_val)  # predict
            ner_result = postprocess.ner_result_format(ner_result)  # format
            predicted_ners[col_name] = ner_result

    assert row_key is not None

    return_json = {
            key_column_name: row_key, 
            "ner": predicted_ners
        }

    if some_q is not None:
        some_q.put(return_json)
    else:
        return return_json
