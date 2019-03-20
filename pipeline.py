import preprocess
import postprocess
import configparser
import compute
import json
import multiprocessing as mp
from multiprocessing.pool import Pool
from multiprocessing.queues import Queue
from functools import partial

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
    print("using single process")

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


def save_clinical_trails_ner_to_file_multi_process(nrows=999, process_num=1):
    print("using multiprocess, process_number is {}".format(args.process_num))

    ner_json_path = config["PATHS"]["ner_json"]
    input_file = config["PATHS"]["clinical_trails_csv"]

    key_column_name = 'nct_id'
    ner_result_generator = compute_ner_from_file_input(
        input_file=input_file, 
        nrows=nrows, 
        key_column_name=key_column_name
    )

    manager = mp.Manager()
    p = Pool(process_num)
    q = manager.Queue()

    def put_to_queue(one_record, some_q):  # worker
        print("getting one record")
        # one_record = next(data_generator)
        print("record got!")
        some_q.put(one_record)
        print("record put!")

    def get_from_queue_and_write(some_q, output_file_path):  # listener
        with open(output_file_path, 'w') as f_json_output:

            ner_result = some_q.get()
            while ner_result is not None:
                f_json_output.write(json.dumps(ner_result) + "\n")

    # start up listener
    print("start listener")
    p.apply_async(get_from_queue_and_write, args=(q, ner_json_path))

    # start up worker
    print("starting worker")
    jobs = []
    for _ in range(process_num):
        job = p.map_async(partial(put_to_queue, some_q=q), ner_result_generator)
        jobs.append(job)

    # collect workers
    for job in jobs:
        job.get()

    # send ending signal
    q.put(None)
    p.close()

if __name__ == "__main__":
    # save_clinical_trails_ner_to_file()
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Decide multiprocess')
    parser.add_argument('--use_mp', help="use multiprocess", action="store_true")
    parser.add_argument('-p', '--process_num', help="pool process number", type=int)

    args = parser.parse_args()

    if args.use_mp:
        save_clinical_trails_ner_to_file_multi_process(process_num=args.process_num)
    else:
        save_clinical_trails_ner_to_file()
