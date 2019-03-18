import configparser

config = configparser.ConfigParser()
config.read("./config.ini")

def get_ner(text):
    """
    Args:
        text - string

    Return:
        ner - dict
    """
    # importing the requests library 
    import requests, json
    
    # api-endpoint 
    URL = "http://{host}:{port}/annotate/text".format(
        host=config["SABER"]["host"],
        port=config["SABER"]["port"] 
    )
    
    # defining a params dict for the parameters to be sent to the API 
    input_data = {'text':text} 

    headers = {'content-type': 'application/json'}
    
    r = requests.post(url=URL, data=json.dumps(input_data), headers=headers) 
    # r.status_code
    ner_result = r.json() 
    
    return ner_result