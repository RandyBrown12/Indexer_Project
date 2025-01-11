import unittest
from unittest.mock import patch
from lib.utilities import decode_tx
from io import StringIO
import os

def greet(name):
    print(f"Hello, {name}!")

#file_path = os.getenv("FILE_PATH")
#file_name = os.getenv("FILE_NAME")
#output_path = os.getenv('txt')
#num = os.getenv('x')

class CheckRetriesForTestBlocks2(unittest.TestCase):
    
    def setUp(self):
        os.environ[''] = f'{os.pwd}/log'
    

    def test(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            greet("Alice")
            self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Alice!")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            greet("World")
            self.assertEqual(mock_stdout.getvalue().strip(), "Hello, World!")
    
    def tearDown(self):
        