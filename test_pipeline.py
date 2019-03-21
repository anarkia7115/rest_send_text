from pprint import pprint
import unittest

class TestPipeline(unittest.TestCase):
    def test_compute_ner_for_clinical_trails(self):
        from pipeline import load_compute_ner
        NUM_OF_ROWS = 2
        row_generator = load_compute_ner(NUM_OF_ROWS, "nct_id")
        row_num = 0
        for _ in row_generator:
            # pprint(row)
            row_num += 1
        self.assertEqual(row_num, NUM_OF_ROWS)

