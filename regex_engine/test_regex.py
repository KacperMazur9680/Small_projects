import unittest
from regex_engine import Regex_Engine

class Test_Regex(unittest.TestCase):

    def test_output(self):
        self.assertEqual(Regex_Engine("^app|apple").compare(), True)
        self.assertEqual(Regex_Engine("le$|apple").compare(), True)
        self.assertEqual(Regex_Engine("^a|apple").compare(), True)
        self.assertEqual(Regex_Engine(".$|apple").compare(), True)
        self.assertEqual(Regex_Engine("apple$|tasty apple").compare(), True)
        self.assertEqual(Regex_Engine("^apple|apple pie").compare(), True)
        self.assertEqual(Regex_Engine("^apple$|apple").compare(), True)
        self.assertEqual(Regex_Engine("^apple$|tasty apple").compare(), False)
        self.assertEqual(Regex_Engine("^apple$|apple pie").compare(), False)
        self.assertEqual(Regex_Engine("app$|apple").compare(), False)
        self.assertEqual(Regex_Engine("^le|apple").compare(), False)
        self.assertEqual(Regex_Engine("a|a").compare(), True)
        self.assertEqual(Regex_Engine(".h|ho").compare(), False)
        self.assertEqual(Regex_Engine("colo.?r|colour").compare(), True)
        self.assertEqual(Regex_Engine("colou?r|colour").compare(), True)
        self.assertEqual(Regex_Engine("colou?r|color").compare(), True)
        self.assertEqual(Regex_Engine("colo.?r|color").compare(), True)
        


if __name__ == "__main__":
    unittest.main()
