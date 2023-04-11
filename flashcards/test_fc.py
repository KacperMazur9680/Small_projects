import unittest 
from unittest.mock import patch
import flashcards

class Test_Flashcards(unittest.TestCase):

    @patch('builtins.input')
    def test_a_simple_add(self, mock_inputs):
        mock_inputs.side_effect = ["1", "What is the capital of Poland", "Warsaw", "2"]
        flashcards.Flashcards().add()

    @patch('builtins.input')
    def test_duplicates(self, mock_inputs):
        fc = flashcards.Flashcards()
        fc.base.update({"What is the capital of Poland": "Warsaw"})
        mock_inputs.side_effect = ["1", "What is the capital of Poland", "What is the capital of England", "Warsaw", "London", "2"]
        fc.add()
    
    

        

if __name__ == "__main__":
    unittest.main()