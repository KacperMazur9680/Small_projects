import unittest 
from unittest.mock import patch, call
import flashcards

class Test_Flashcards(unittest.TestCase):

    @patch('builtins.print')
    @patch('builtins.input')
    def test_1_add(self, mock_inputs, mock_print):
        mock_inputs.side_effect = ["1", "What is the capital of Poland", "Warsaw", "2"]
        flashcards.Flashcards().add()
        
        self.assertEqual(mock_print.mock_calls, [call('The card ("What is the capital of Poland":"Warsaw") has been added.'), call()])

    @patch('builtins.print')
    @patch('builtins.input')
    def test_2_duplicates(self, mock_inputs, mock_prints):
        fc = flashcards.Flashcards()
        fc.base.update({"What is the capital of Poland": "Warsaw"})

        mock_inputs.side_effect = ["1", "What is the capital of Poland", "What is the capital of England", "Warsaw", "London", "2"]
        fc.add()

        self.assertEqual(mock_prints.mock_calls, [call('The term "What is the capital of Poland" already exists. Try again:'),
                                                 call('The definition "Warsaw" already exists. Try again:'),
                                                 call('The card ("What is the capital of England":"London") has been added.'),
                                                 call()])
    
    @patch('builtins.print')
    def test_3_ask_empty_dict(self, mock_print):
        flashcards.Flashcards().ask()
        self.assertEqual(mock_print.mock_calls, [call("\nThere are no flashcards to practice!\n")])

    @patch("builtins.print")
    @patch("builtins.input")
    def test_4_ask(self, mock_inputs, mock_prints):
        fc = flashcards.Flashcards()
        fc.base.update({"What is the capital of Poland": "Warsaw",
                        "What is the capital of UK":"London",
                        "What is the capital of Brazil":"Brasilia",
                        "What is the capital of Germany":"Berlin"})
        fc.wrong_ans_base.update({"What is the capital of Germany":0})

        mock_inputs.side_effect = ["4", "Warsaw", "y", "n", "Moscow"]
        fc.ask()

        self.assertEqual(mock_prints.mock_calls, [call("Correct!\n"),
                                                  call("Answer: London\n"),
                                                  call('Wrong. The right answer is "Berlin".'),
                                                  call()])



        

if __name__ == "__main__":
    unittest.main()