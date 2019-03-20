from pprint import pprint
import unittest

class TestPipeline(unittest.TestCase):
    def test_compute_ner_for_clinical_trails(self):
        from pipeline import compute_ner_for_clinical_trails
        NUM_OF_ROWS = 2
        row_generator = compute_ner_for_clinical_trails(NUM_OF_ROWS, "nct_id")
        row_num = 0
        for row in row_generator:
            # pprint(row)
            row_num += 1
        self.assertEqual(row_num, NUM_OF_ROWS)

