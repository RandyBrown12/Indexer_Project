import unittest
from unittest.mock import patch
from lib.utilities import decode_tx
from io import StringIO

def greet(name):
    print(f"Hello, {name}!")

class CheckRetriesForTestBlocks2(unittest.TestCase):
    def test(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            greet("Alice")
            self.assertEqual(mock_stdout.getvalue().strip(), "Hello, Alice")