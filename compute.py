import configparser
import time
import requests, json


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