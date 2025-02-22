import unittest
from lib.utilities import decode_tx
from unittest.mock import patch, MagicMock
import requests
import os

class Validate_Decode_Tx_Function(unittest.TestCase):
    valid_tx_string = "Cu4CCtUCCiQvY29zbXdhc20ud2FzbS52MS5Nc2dFeGVjdXRlQ29udHJhY3QSrAIKLm1pZ2Fsb28xeWx4MDN2cXAyemtwamF5dWRweDJrMHBzZ2R4NHVjM2RtdXM4MmQSQm1pZ2Fsb28xbTdudDB6eHVmM2p2ajJrOGg5a21na3hqbWVweHozazl0MmM5Y2U4eHdqOTRjc2cwZXB2cTVqNnozdxq1AXsidm90ZSI6eyJ2b3RlcyI6W1sibmF0aXZlOmZhY3RvcnkvbWlnYWxvbzFlcW50bmw2dHpjajloODZwc2c0eTRoNmhoMDVnMmg5bmo4ZTA5bC91cmFjIiw2MDAwXSxbIm5hdGl2ZTppYmMvRUM0OEI4MTlGQzFEOTU1RUQxNzA4QThFOEUyMzBCMzcyMTdDQzZEOTUzNDQ4RDNCNEJDQ0Y1QjI5QkQxRkNGOSIsNDAwMF1dfX0SFHd3dy5lcmlzcHJvdG9jb2wuY29tEmsKUQpGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQNzmL8lOV00cHsfkASseu2+cwLwBHlCfv0MVCIpk2QcIxIECgIIARjhAhIWChAKBnV3aGFsZRIGNjgxOTk2EIrYIhpAHrBm4x5/qFaaR73GMq/vXDE6Tn7QT+Lcv47tQxbZVJI5qrx72gKSsg8oetjdWAHi0QNyH7D4/ipfBWwhBxFGjA=="
    valid_json = {'tx':{'body':{'messages':[{'@type':'/cosmwasm.wasm.v1.MsgExecuteContract','sender':'migaloo1ylx03vqp2zkpjayudpx2k0psgdx4uc3dmus82d','contract':'migaloo1m7nt0zxuf3jvj2k8h9kmgkxjmepxz3k9t2c9ce8xwj94csg0epvq5j6z3w','msg':{'vote':{'votes':[['native:factory/migaloo1eqntnl6tzcj9h86psg4y4h6hh05g2h9nj8e09l/urac',6000],['native:ibc/EC48B819FC1D955ED1708A8E8E230B37217CC6D953448D3B4BCCF5B29BD1FCF9',4000]]}},'funds':[]}],'memo':'www.erisprotocol.com','timeout_height':'0','extension_options':[],'non_critical_extension_options':[]},'auth_info':{'signer_infos':[{'public_key':{'@type':'/cosmos.crypto.secp256k1.PubKey','key':'A3OYvyU5XTRwex+QBKx67b5zAvAEeUJ+/QxUIimTZBwj'},'mode_info':{'single':{'mode':'SIGN_MODE_DIRECT'}},'sequence':'353'}],'fee':{'amount':[{'denom':'uwhale','amount':'681996'}],'gas_limit':'568330','payer':'','granter':''},'tip':None},'signatures':['HrBm4x5/qFaaR73GMq/vXDE6Tn7QT+Lcv47tQxbZVJI5qrx72gKSsg8oetjdWAHi0QNyH7D4/ipfBWwhBxFGjA==']}}    
    
    def test_successful_base64_decode(self):
        self.assertDictEqual(decode_tx(self.valid_tx_string), self.valid_json)
    
    @patch.dict(os.environ, {"FILE_NAME": "9999997" })
    def test_failed_base64_decode(self):
        self.assertEqual(decode_tx("abc"), None)

    # Test a return code of 200 series other than 200.
    @patch('requests.post')
    def test_202_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.json.return_value = self.valid_json
        mock_get.return_value = mock_response
        decode_tx(self.valid_tx_string)
        self.assertEqual(mock_get.call_count, 9)

    # Go to one endpoint on 400 errors.
    @patch.dict(os.environ, {"FILE_NAME": "9999998" })
    @patch('requests.post')
    def test_400_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = self.valid_json
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "401 Client Error: Bad Request for url: MockedDataURL"
        )
        mock_get.return_value = mock_response
        decode_tx(self.valid_tx_string)
        self.assertEqual(mock_get.call_count, 1)

    # Go to different endpoints 9 times on 500 errors.
    @patch.dict(os.environ, {"FILE_NAME": "9999999" })
    @patch('requests.post')
    def test_500_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = self.valid_json
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "500 Server Error: Bad Request for url: MockedDataURL"
        )
        mock_get.return_value = mock_response
        decode_tx(self.valid_tx_string, retry_delay=1)
        self.assertEqual(mock_get.call_count, 9)

if __name__ == "__main__":
    unittest.main()