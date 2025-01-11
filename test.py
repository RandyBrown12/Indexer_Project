
import requests
import json

def decode_tx(tx):
        url_array = ["https://lcd-terra.wildsage.io", "https://phoenix-lcd.terra.dev:443", "https://api-terra.cosmos-spaces.cloud", "https://api-terra-01.stakeflow.io", "https://terra-phoenix-api.highstakes.ch", "https://terra-api.polkachu.com"]
        
        full_url = url_array[4] + "/cosmos/tx/v1beta1/decode"
        #Not implemented : url = "https://phoenix-lcd.terra.dev/cosmos/tx/v1beta1/decode"
        #Not implemented : url = "https://lcd-terra.tfl.foundation/cosmos/tx/v1beta1/decode"
        #url = "https://terra-rest.publicnode.com/cosmos/tx/v1beta1/decode"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"tx_bytes": tx})

        response = requests.post(full_url, headers=headers, data=data)
        print(response)
        return(response.json())

# examples of code.

code = "CpwgCukfCh0vY29zbW9zLmF1dGh6LnYxYmV0YTEuTXNnRXhlYxLHHwoubWlnYWxvbzE5NHl0bjUweWhoNjdyZGhhOGFraHM3YzZ6dWxuejRuMnlycWVlZBKcAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdQoubWlnYWxvbzFxZTg2ZjhydDNobHpzc3BmN2VmcTNoMGMzZGxzeWZxd3hoMzM0YxI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDAoGdXdoYWxlEgI2MhKcAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdQoubWlnYWxvbzFwZW1rMjl3ZTNrZ3VmM25sZXBkcHBlemo3NXZkd2p3dXN6dHhucxI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDAoGdXdoYWxlEgIyMRKbAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdAoubWlnYWxvbzFxczRlcXRjMGYyODk0M3M5cThqemNuY3I1cGttY2drZnYyMnlzaxI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaCwoGdXdoYWxlEgExEpsBCiMvY29zbW9zLnN0YWtpbmcudjFiZXRhMS5Nc2dEZWxlZ2F0ZRJ0Ci5taWdhbG9vMXEzOHc3ZnEyOTg5OWtzNjVwcXk3OG11bGh5endqdDRkY215NGpkEjVtaWdhbG9vdmFsb3BlcjF6Y2c2N2p1MmczZmx1dzVhZDQ2cG54eDV3NnNkbnowanNnbGs3MBoLCgZ1d2hhbGUSATMSmwEKIy9jb3Ntb3Muc3Rha2luZy52MWJldGExLk1zZ0RlbGVnYXRlEnQKLm1pZ2Fsb28xcGpkMmQydWZ0OWtmNnJ3cHY0eGw2N2pmOHFsaGV0d3duMGgwZWsSNW1pZ2Fsb292YWxvcGVyMXpjZzY3anUyZzNmbHV3NWFkNDZwbnh4NXc2c2RuejBqc2dsazcwGgsKBnV3aGFsZRIBNRKcAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdQoubWlnYWxvbzFwOGZ4MHh2MmNmbjhkdXVhaHU4a3N5YXR6c2VtbXVwdG41dDB5dRI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDAoGdXdoYWxlEgIxMBKcAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdQoubWlnYWxvbzFxcjg1bHpyNmRtYTdyMGtrNGU5a3JtOTV2bG5nbjQ5bmowbHN2ORI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDAoGdXdoYWxlEgIxORKeAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdwoubWlnYWxvbzFxeWZsZWQ1dWxmNndtdTJ1NHNtc3RuOHJsemF6YW5tcTQ4eDd6YRI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDgoGdXdoYWxlEgQxMDcxEp0BCiMvY29zbW9zLnN0YWtpbmcudjFiZXRhMS5Nc2dEZWxlZ2F0ZRJ2Ci5taWdhbG9vMXAwczdxZ2FqZmpwaDI0eWpsM2pqMDlmbmNweGpueGZteHp1cXY2EjVtaWdhbG9vdmFsb3BlcjF6Y2c2N2p1MmczZmx1dzVhZDQ2cG54eDV3NnNkbnowanNnbGs3MBoNCgZ1d2hhbGUSAzgwOBKcAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdQoubWlnYWxvbzFxanp6dTBwZDljNDdrNmt2bDhmM21majBoZTY3eHdrZjIyeDVsdRI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDAoGdXdoYWxlEgI3MRKcAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdQoubWlnYWxvbzFxM2gwNmsyaGp2czRrNXNyODQ0Y3N0dW55d3R3OXV2bHg1cDIwZhI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDAoGdXdoYWxlEgIxMBKeAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdwoubWlnYWxvbzFydHkyZWpteXd3Z2t1Z21xd2NubTMzNjVyeWc0aHlsd2czcmtweBI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDgoGdXdoYWxlEgQxNjU0Ep0BCiMvY29zbW9zLnN0YWtpbmcudjFiZXRhMS5Nc2dEZWxlZ2F0ZRJ2Ci5taWdhbG9vMXA4MHk0dDRjdDU3c3Y3MGttZHl4YWxtcmtocDZzc2R0OGVjd2w0EjVtaWdhbG9vdmFsb3BlcjF6Y2c2N2p1MmczZmx1dzVhZDQ2cG54eDV3NnNkbnowanNnbGs3MBoNCgZ1d2hhbGUSAzExORKdAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdgoubWlnYWxvbzFxenUzNHh3OWhoNWpuZHFzZXg3M2d5ZGpucjVjazZnajh6OW5tMhI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDQoGdXdoYWxlEgMxNjESnAEKIy9jb3Ntb3Muc3Rha2luZy52MWJldGExLk1zZ0RlbGVnYXRlEnUKLm1pZ2Fsb28xenNjbDN1a2M1cDZoN3RoMDBrZHk4ajBkY3Buc3FrbGdmZTh1ZjkSNW1pZ2Fsb292YWxvcGVyMXpjZzY3anUyZzNmbHV3NWFkNDZwbnh4NXc2c2RuejBqc2dsazcwGgwKBnV3aGFsZRICMTESnQEKIy9jb3Ntb3Muc3Rha2luZy52MWJldGExLk1zZ0RlbGVnYXRlEnYKLm1pZ2Fsb28xcnQ5d2V3dGpyeDkzMDU2NWdleTU3cThkNXc1YXN2cjl3bm54MG4SNW1pZ2Fsb292YWxvcGVyMXpjZzY3anUyZzNmbHV3NWFkNDZwbnh4NXc2c2RuejBqc2dsazcwGg0KBnV3aGFsZRIDNTM3Ep0BCiMvY29zbW9zLnN0YWtpbmcudjFiZXRhMS5Nc2dEZWxlZ2F0ZRJ2Ci5taWdhbG9vMXp4eDhqNzVuZ204bTM4djlsNXdyZWFhdnduc3V1bjdndW1nazR2EjVtaWdhbG9vdmFsb3BlcjF6Y2c2N2p1MmczZmx1dzVhZDQ2cG54eDV3NnNkbnowanNnbGs3MBoNCgZ1d2hhbGUSAzE3NxKeAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdwoubWlnYWxvbzFwYXNsdmo2em5reWhwY2EybHVndmhsc3hrcXRlcGp4eGQwOHEyMhI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDgoGdXdoYWxlEgQxMDE0Ep0BCiMvY29zbW9zLnN0YWtpbmcudjFiZXRhMS5Nc2dEZWxlZ2F0ZRJ2Ci5taWdhbG9vMXptZDJkZ3JoMjVyMzlmMHJqNDA0anpzcTl0cnE3NmNkcHN2N3Z5EjVtaWdhbG9vdmFsb3BlcjF6Y2c2N2p1MmczZmx1dzVhZDQ2cG54eDV3NnNkbnowanNnbGs3MBoNCgZ1d2hhbGUSAzIzMhKdAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdgoubWlnYWxvbzF6eGdyeGo5Z2ZzMzRkcDd6cnA2c3E3NHlkemhsdWx0bmMzNHd2ZhI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDQoGdXdoYWxlEgM4NTMSnQEKIy9jb3Ntb3Muc3Rha2luZy52MWJldGExLk1zZ0RlbGVnYXRlEnYKLm1pZ2Fsb28xcGd2YTU4dndoZDh5NGo0OWtxZnR3a3pjd3VtcmhjbjdwbTZzdjgSNW1pZ2Fsb292YWxvcGVyMXpjZzY3anUyZzNmbHV3NWFkNDZwbnh4NXc2c2RuejBqc2dsazcwGg0KBnV3aGFsZRIDNTM3Ep4BCiMvY29zbW9zLnN0YWtpbmcudjFiZXRhMS5Nc2dEZWxlZ2F0ZRJ3Ci5taWdhbG9vMXI2eXZ4aDM5OXlnOTc3dXcyOHFjeGptYWg0dDZzNTZhcHh5eGxxEjVtaWdhbG9vdmFsb3BlcjF6Y2c2N2p1MmczZmx1dzVhZDQ2cG54eDV3NnNkbnowanNnbGs3MBoOCgZ1d2hhbGUSBDE0NDISmwEKIy9jb3Ntb3Muc3Rha2luZy52MWJldGExLk1zZ0RlbGVnYXRlEnQKLm1pZ2Fsb28xeXNzcnV4ODk5bDBubHpjY3o1MHN3anozaHNreWR5cWFzbHg4cmoSNW1pZ2Fsb292YWxvcGVyMXpjZzY3anUyZzNmbHV3NWFkNDZwbnh4NXc2c2RuejBqc2dsazcwGgsKBnV3aGFsZRIBMRKeAQojL2Nvc21vcy5zdGFraW5nLnYxYmV0YTEuTXNnRGVsZWdhdGUSdwoubWlnYWxvbzFyM215NnAzOWxtbXUybGVrYzBwZGFlNm1qNDZkZWYyNWRwYzhkdxI1bWlnYWxvb3ZhbG9wZXIxemNnNjdqdTJnM2ZsdXc1YWQ0NnBueHg1dzZzZG56MGpzZ2xrNzAaDgoGdXdoYWxlEgQyNjYwEp4BCiMvY29zbW9zLnN0YWtpbmcudjFiZXRhMS5Nc2dEZWxlZ2F0ZRJ3Ci5taWdhbG9vMTlmamt2Yzdxa3E2dGFqMzl5a3B5cGp3aG1kY3p3dmM1dHRrcndlEjVtaWdhbG9vdmFsb3BlcjF6Y2c2N2p1MmczZmx1dzVhZDQ2cG54eDV3NnNkbnowanNnbGs3MBoOCgZ1d2hhbGUSBDI5NzYSLlJFU3Rha2VkIGJ5ICBBdXRvU3Rha2Ug8J+boe+4jyBTbGFzaCBQcm90ZWN0ZWQSaApSCkYKHy9jb3Ntb3MuY3J5cHRvLnNlY3AyNTZrMS5QdWJLZXkSIwohA5pdj0XXSPm4/wdyFYE4snAiwjomXME+ZjtnmsS60HXjEgQKAggBGLzSJhISCgsKBnV3aGFsZRIBNxD4u4kDGkCO+qdOTqe3cvdLbBFnVbkYQl2X8q1yjc0tQSZp79twN0A3v+YhKHAl5FhXp79fpdMH3Z5uPAJh65h/6mkUXpoO"



# if $code contain multiple elements(transactions), split it
code = code.split()
many = len(code)
print(many)

for i in range(many):
    # let decoded_response be the decoded string
    decoded_response = decode_tx(code[i])

    # Print it in JSON type-
    print(f'Here is number {i+1} transaction\n')
    print(json.dumps(decoded_response, indent=2))


