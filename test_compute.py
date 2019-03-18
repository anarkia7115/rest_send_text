import unittest

class TestCompute(unittest.TestCase):

    def test_ner(self):
        import compute
        # get test data
        import preprocess
        clinical_trails_df = preprocess.load_clinical_trails()
        clinical_trails_df = preprocess.keep_text_fileds(clinical_trails_df)

        col_num = 1
        sample_text = clinical_trails_df.take([0])[clinical_trails_df.columns[col_num]].values[0]
        self.assertEqual(type(sample_text), str)

        ner_result = compute.get_ner(sample_text)
        print(ner_result)
