import base64, zlib, json

data = "eJxVjMsOgyAQRf-FtSGADILLrrrpNxB0hkof2IgmTZr-ezUxTdyee879sKXQlMOTWMvOlDCx6o88vV9pouLDzFrZNM46LZXj0mkjTMV8WObBb7ZPuPaKHVgX-jvlbcBbyNeR92Oep9TxTeH7WvhlRHqcdvdwMIQyrHVsAHRUskGJQLWOGnSnsTcA0qKorQEyEmIIIBQYdLVD0FZY5YyIAtn3B2M_SRE"

data = data.replace('-', '+').replace('_', '/')
data += '=' * (4 - len(data) % 4)

def test():
 
    print(json.loads(zlib.decompress(base64.b64decode(data)).decode()))

test()