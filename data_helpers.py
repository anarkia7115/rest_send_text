import json
def dict_save(row_generator, output_file):
    with open(output_file, 'w') as fw:
        for row in row_generator:
            row_json = json.dumps(row)
            fw.write(row_json+"\n")


def dict_load(row_records_file):
    with open(row_records_file) as f_in:
        for row in f_in:
            row_json = json.loads(row)
            yield row_json
