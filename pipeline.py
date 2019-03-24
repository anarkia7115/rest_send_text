import preprocess
import postprocess
import configparser
import compute
import json
import multiprocessing as mp
from multiprocessing import Pool
from functools import partial
import data_helpers

config = configparser.ConfigParser()
config.read("./config.ini")

STOP_SIGNAL="KILL"

def load_compute_ner(nrows, 
        key_column_name, 
        predictor=compute.get_ner):
    """
    Params:
        predictor - predictor function: ner = predictor(input_text)

    1. load text
    2. process every list, predict ner
    3. yield prediction value
    """
    ct_text_rows = preprocess.load_clinical_trails_text(nrows=nrows, returntype='dict')

    num_of_rows = 0

    for row in ct_text_rows:

        row_key, predicted_ners = compute.ner_for_row(
            row, key_column_name, predictor
        )
        assert row_key is not None

        num_of_rows += 1
        print("{} rows processed".format(num_of_rows))

        yield {
            key_column_name: row_key, 
            "ner": predicted_ners
        }

def load_and_compute_ner_multi_process(
        nrows, 
        key_column_name,
        process_pool:Pool, 
        some_q,
        predictor=compute.get_ner):
    """
    Params:
        predictor - predictor function: ner = predictor(input_text)

    1. load text
    2. process every list, predict ner
    3. yield prediction value
    """
    ct_text_rows = preprocess.load_clinical_trails_text(nrows=nrows, returntype='dict')
    ct_text_rows = list(ct_text_rows)

    # worker async
    print("starting workers")
    
    print("job started!")
    process_pool.map(
        partial(
            compute.ner_for_row, 
            key_column_name=key_column_name,
            predictor=predictor, 
            some_q=some_q), 
        ct_text_rows)

    # collecting
    print("job finished!")

    # send ending signal
    print("sending end signal")
    some_q.put(None)

    # returns in some_q

def save_clinical_trails_ner_to_file(nrows=999):
    print("using single process")

    ner_json_path = config["PATHS"]["ner_json"]

    key_column_name = 'nct_id'
    ner_result_generator = load_compute_ner(
        nrows=nrows, 
        key_column_name=key_column_name
    )

    with open(ner_json_path, 'w') as f_json_output:
        for ner_result in ner_result_generator:
            f_json_output.write(json.dumps(ner_result) + "\n")

def put_to_queue(data_generator, some_q):  # worker
    print("getting one record")
    one_record = next(data_generator)
    print("record got!")
    some_q.put(one_record)
    print("record put!")

def get_from_queue_and_write(some_q, output_file_path, stop_signal):  # listener
    f_json_output = open(output_file_path, 'w')
    print("start listener")
    while True:
        print("waiting from q")
        ner_result = some_q.get()
        if ner_result == stop_signal:
            break
        try:
            f_json_output.write(json.dumps(ner_result) + "\n")
        except Exception as e:
            print("Error when parsing json, just pass: "+str(e))
            pass
        f_json_output.flush()
    f_json_output.close()

def save_clinical_trails_ner_to_file_multi_process(nrows=999, process_num=1):
    print("using multiprocess, process_number is {}".format(args.process_num))

    ner_json_path = config["PATHS"]["ner_json"]

    key_column_name = 'nct_id'

    p = Pool(process_num)
    manager = mp.Manager()
    q = manager.Queue()

    # start up listener
    print("start listener")
    p.apply_async(get_from_queue_and_write, args=(q, ner_json_path, STOP_SIGNAL))

    # start up worker
    load_and_compute_ner_multi_process(
        nrows, 
        key_column_name, 
        p, q)
    
    # finished
    q.put(STOP_SIGNAL)
    p.close()


if __name__ == "__main__":
    import multiprocessing, logging
    mpl = multiprocessing.log_to_stderr()
    mpl.setLevel(logging.INFO)

    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Decide multiprocess')
    parser.add_argument('--use_mp', help="use multiprocess", action="store_true")
    parser.add_argument('-p', '--process_num', help="pool process number", type=int)
    parser.add_argument('-n', '--nrows', help="limit row of numbers", type=int, default=None)

    args = parser.parse_args()

    if args.use_mp:
        save_clinical_trails_ner_to_file_multi_process(nrows=args.nrows, process_num=args.process_num)
    else:
        save_clinical_trails_ner_to_file(nrows=args.nrows)
