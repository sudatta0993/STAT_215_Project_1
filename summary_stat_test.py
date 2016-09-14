import unittest
import pandas as pd
from summary_stat import mean_in_triplet

class summary_stat__test_case(unittest.TestCase):

    def test_with_existing(self):
        "Checking if method works when mean is present"
        data = pd.DataFrame(columns=['col1', 'col2', 'col3','average'])
        data = data.append({'col1': 2, 'col2': 3, 'col3': 4, 'average': 3}, ignore_index=True)
        self.assertTrue(mean_in_triplet(data,'col1','col2','col3','average') == 1)

    def test_without_existing(self):
        "Checking if method works when mean is NOT present"
        data = pd.DataFrame(columns=['col1', 'col2', 'col3', 'average'])
        data = data.append({'col1': 2, 'col2': 5, 'col3': 11, 'average': 6}, ignore_index=True)
        self.assertTrue(mean_in_triplet(data, 'col1', 'col2', 'col3', 'average') == 0)