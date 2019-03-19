import unittest

class TestCompute(unittest.TestCase):

    def test_ner(self):
        import compute
        # get test data
        import preprocess
        clinical_trails_df = preprocess.load_clinical_trails()
        clinical_trails_df = preprocess.keep_text_fileds(clinical_trails_df)

        record_idx = 0
        col_num = 2
        sample_text = list(list(clinical_trails_df)[record_idx].values())[col_num]
        self.assertEqual(type(sample_text), str)

        ner_result = compute.get_ner(sample_text)
        print(ner_result)
