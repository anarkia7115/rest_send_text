import configparser
import time
import requests, json
import postprocess
from multiprocessing import Queue
import multiprocessing as mp
from pprint import pprint
import data_helpers

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
    try:
        ner_result = r.json() 
    except json.decoder.JSONDecodeError:
        print("cannot parse request:")
        pprint(r)
        pprint(r.text)
        ner_result = None
        # TODO: improve error handling
    
    print("--- %s seconds in ner ---" % (time.time() - start_time))
    return ner_result


def map_json_records(
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

    cpname = mp.current_process().name
    # print cpname
    print("{0} is currently doing...".format(cpname))
    row_key, predicted_ners = data_helpers.map_dict_value(
        row, 
        key_column_name, 
        lambda x: postprocess.ner_result_format(predictor(x)))

    return_json = {
            key_column_name: row_key, 
            "ner": predicted_ners
        }

    if some_q is not None:
        print("put result to q")
        some_q.put(return_json)
    else:
        return return_json
