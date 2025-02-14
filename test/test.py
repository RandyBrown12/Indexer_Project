import unittest
from lib.utilities import decode_tx, log_error_to_database
import json
#file_path = os.getenv("FILE_PATH")
#file_name = os.getenv("FILE_NAME")
#num = os.getenv('x')

class Validate_Decode_Tx_Function(unittest.TestCase):
    
    # Test a valid json
    def test_base64_decode(self):
        valid_tx_string = "Cu4CCtUCCiQvY29zbXdhc20ud2FzbS52MS5Nc2dFeGVjdXRlQ29udHJhY3QSrAIKLm1pZ2Fsb28xeWx4MDN2cXAyemtwamF5dWRweDJrMHBzZ2R4NHVjM2RtdXM4MmQSQm1pZ2Fsb28xbTdudDB6eHVmM2p2ajJrOGg5a21na3hqbWVweHozazl0MmM5Y2U4eHdqOTRjc2cwZXB2cTVqNnozdxq1AXsidm90ZSI6eyJ2b3RlcyI6W1sibmF0aXZlOmZhY3RvcnkvbWlnYWxvbzFlcW50bmw2dHpjajloODZwc2c0eTRoNmhoMDVnMmg5bmo4ZTA5bC91cmFjIiw2MDAwXSxbIm5hdGl2ZTppYmMvRUM0OEI4MTlGQzFEOTU1RUQxNzA4QThFOEUyMzBCMzcyMTdDQzZEOTUzNDQ4RDNCNEJDQ0Y1QjI5QkQxRkNGOSIsNDAwMF1dfX0SFHd3dy5lcmlzcHJvdG9jb2wuY29tEmsKUQpGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQNzmL8lOV00cHsfkASseu2+cwLwBHlCfv0MVCIpk2QcIxIECgIIARjhAhIWChAKBnV3aGFsZRIGNjgxOTk2EIrYIhpAHrBm4x5/qFaaR73GMq/vXDE6Tn7QT+Lcv47tQxbZVJI5qrx72gKSsg8oetjdWAHi0QNyH7D4/ipfBWwhBxFGjA=="
        valid_json = {'tx':{'body':{'messages':[{'@type':'/cosmwasm.wasm.v1.MsgExecuteContract','sender':'migaloo1ylx03vqp2zkpjayudpx2k0psgdx4uc3dmus82d','contract':'migaloo1m7nt0zxuf3jvj2k8h9kmgkxjmepxz3k9t2c9ce8xwj94csg0epvq5j6z3w','msg':{'vote':{'votes':[['native:factory/migaloo1eqntnl6tzcj9h86psg4y4h6hh05g2h9nj8e09l/urac',6000],['native:ibc/EC48B819FC1D955ED1708A8E8E230B37217CC6D953448D3B4BCCF5B29BD1FCF9',4000]]}},'funds':[]}],'memo':'www.erisprotocol.com','timeout_height':'0','extension_options':[],'non_critical_extension_options':[]},'auth_info':{'signer_infos':[{'public_key':{'@type':'/cosmos.crypto.secp256k1.PubKey','key':'A3OYvyU5XTRwex+QBKx67b5zAvAEeUJ+/QxUIimTZBwj'},'mode_info':{'single':{'mode':'SIGN_MODE_DIRECT'}},'sequence':'353'}],'fee':{'amount':[{'denom':'uwhale','amount':'681996'}],'gas_limit':'568330','payer':'','granter':''},'tip':None},'signatures':['HrBm4x5/qFaaR73GMq/vXDE6Tn7QT+Lcv47tQxbZVJI5qrx72gKSsg8oetjdWAHi0QNyH7D4/ipfBWwhBxFGjA==']}}
        self.assertDictEqual(decode_tx(valid_tx_string), valid_json)
        
    def test_invalid_base64(self):
        self.assertEqual(decode_tx("abc"), None)

    def test_logging(self):
        tx_string = "CrgBCqMBCiQvY29zbXdhc20ud2FzbS52MS5Nc2dNaWdyYXRlQ29udHJhY3QSewoubWlnYWxvbzE4cTZleXo1c3VyODU5cHl1NjU2ZnUyazJsaG1sN3U2YXljeG1tNhJCbWlnYWxvbzFyOHEwMmF3ZGM0ajRwOTdoM21nc3I3ODQ0cDRkMjB6eW1mcXA0cmc2cHJnbGo4N3I5N3Zxd3ptbWQzGJcGIgJ7fRIQTWlncmF0ZSBDb250cmFjdBJqClAKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiECuHbppNsIwXwBnPtUotd3ldo6/rqQEWSVXIhzMvU5bIYSBAoCCAEYOhIWChAKBnV3aGFsZRIGMTYzMzk0EML8CRpATyhvZqCKnzFd26FMIuB1XN53iarvCUdb/eFfJk97HxBX00cvqo0wgqGwF8t0D3W4xz89iOHL1sT87Yfvg0CfzQ=="
        print(decode_tx(tx_string))
        
if __name__ == "__main__":
    unittest.main()