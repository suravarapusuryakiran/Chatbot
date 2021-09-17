from tests.my_custom_functions import get_link_from_tc
import unittest
import pickle
import pandas as pd



class TestStringMethods(unittest.TestCase):

    def test_pickle_load(self):
        with open('actions\new_data_pickle.pkl','rb') as pickle_file:
            pickle_database_lookup=pd.DataFrame()
            pickle_database_lookup=pickle.load(pickle_file)
            print(pickle_database_lookup["Material"])
            



    def test_cytropac_base_link(self):
        """
            AS YOU CAN SEE BELOW
            THE TEST CASE RAN SUCCESSFUL --> Ran 1 test 
            OK
        """
        self.assertEqual(get_link_from_tc("CYTROPAC"), "my_cytropac_link")

    def test_cytropac_cad_link(self):
        """
            THIS FUNCTION IS NOT IMPLEMENTED YET
            THIS WILLTHROW AN ERROR
        """
        self.assertEqual(get_link_from_tc("CYTROPAC-1x/20/AF"), "specific_cytropac_link")
        self.assertEqual(get_link_from_tc("CYTROPAC-1x/20/ST"), "specific_cytropac_link")


if __name__ == '__main__':
    unittest.main()
