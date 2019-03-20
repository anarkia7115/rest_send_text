import unittest

class TestPreprocess(unittest.TestCase):

    def test_clinical_trails_df_loaded(self):
        import preprocess, pandas as pd
        df = preprocess.load_clinical_trails()
        self.assertTrue(type(df), pd.DataFrame)
        df = preprocess.keep_text_fileds(df)

    def test_load_as_dict(self):
        import preprocess
        clinical_trails_record_generator = preprocess.load_clinical_trails(return_type="dict")
        MAX = 1
        i = 0
        from pprint import pprint
        print(type(clinical_trails_record_generator))
        for record in clinical_trails_record_generator:
            # pprint(record)
            if i > MAX:
                break
            i += 1 

    def test_keep_text_field(self):
        import preprocess
        clinical_trails_record_generator = preprocess.load_clinical_trails(return_type="dict")
        text_fields_only = preprocess.keep_text_fileds(clinical_trails_record_generator)
        MAX = 1
        i = 0
        from pprint import pprint
        print(type(text_fields_only))
        for record in text_fields_only:
            # pprint(record)
            if i > MAX:
                break
            i += 1 
