import unittest

import configparser
config = configparser.ConfigParser()
config.read("./config.ini")

class TestDataHelpers(unittest.TestCase):
    def test_json_record_to_bioc(self):
        from data_helpers import json_record_to_bioc
        row_id = "112233aabbcc.123abc"
        row_content = "here is some row content"
        REP_TIMES = 5
        for _ in range(REP_TIMES):
            print(json_record_to_bioc(row_content).format(
                row_id=row_id, col_name="aaa_colname"))

    def test_bioc_to_json_records(self):
        from data_helpers import bioc_to_json_records
        pubtator_path = config["PATHS"]["test_dh_pubtator"]
        with open(pubtator_path, encoding='utf8') as f_in:
            for content in f_in:
                ner_json = bioc_to_json_records(content.strip())
                if ner_json is not None:
                    print(ner_json)

