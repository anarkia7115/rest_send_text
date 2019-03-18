import unittest

class TestPreprocess(unittest.TestCase):

    def test_clinical_trails_df_loaded(self):
        import preprocess, pandas as pd
        df = preprocess.load_clinical_trails()
        self.assertTrue(type(df), pd.DataFrame)
        df = preprocess.keep_text_fileds(df)
        self.assertEqual(len(df.columns), 4)