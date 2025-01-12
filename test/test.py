import unittest
from unittest.mock import patch
from ..lib.utilities import decode_tx
from io import StringIO
import os

#file_path = os.getenv("FILE_PATH")
#file_name = os.getenv("FILE_NAME")
#num = os.getenv('x')

class CheckRetriesForTestBlocks2(unittest.TestCase):
    
    def test(self):

        ENV_VARIABLES = {
            "FILE_PATH":'./test/test_blocks2',
            "FILE_NAME":'7138068',
            "x":'7138068'
        }

        with patch.dict(os.environ, ENV_VARIABLES):
            decode_tx()