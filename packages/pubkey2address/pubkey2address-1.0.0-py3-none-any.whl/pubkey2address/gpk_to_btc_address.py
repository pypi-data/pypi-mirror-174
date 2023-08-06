from bit import  format
class GPK2BTCADDRESS:
    def __init__(self,gpk_curve:dict,net = 'main'):
        '''
        support BTC/LTC/DOGE
        :param gpk_curve:
            {
                "curve1": "1",
                "curve2": "0",
                "gpk1": "0x0c440bf2b594bdf526cbbcaae75dcb5f93d1f9bdd2f234f853fe4acf5f0e2d6d0525ad07f29f86943bc7c356a80e08e7345b12bc9bf5eb10e9d787b478f5ebb3",
                "gpk2": "0x273c3273c072f826f728f865d58ccd297b293b87045fd806973d2a4d82f220a072bc5240c7d5920e0ddfdb0e01aeba184de9ef8ae14f5748243d8fa58d28e136"
            }
        :return:
        '''
        self.net = net
        self.gpk_curve = gpk_curve
        self.type = \
            {
            "BTC":{"test":b'\x6f',"main": b'\x00'},
            "LTC":{'test':b'\x6f',"main": b'\x30'},
            "DOGE":{"test":b'q',"main": b'\x1e'}
            }
        if gpk_curve['curve1'] == 0:
            gpk = gpk_curve['gpk1']
        else:
            gpk = gpk_curve['gpk2']

        self.public_key_hex = '04' + gpk[2::]
    def public_key_to_address(self, chain):
        '''
        :return:
        '''

        public_key = bytes.fromhex(self.public_key_hex)
        version = self.type[chain][self.net]
        length = len(public_key)
        if length not in (33, 65):
            raise ValueError('{} is an invalid length for a public key.'.format(length))
        return format.b58encode_check(version + format.ripemd160_sha256(public_key))

if __name__ == '__main__':
    gr =  {
                "curve1": "1",
                "curve2": "0",
                "gpk1": "0x0c440bf2b594bdf526cbbcaae75dcb5f93d1f9bdd2f234f853fe4acf5f0e2d6d0525ad07f29f86943bc7c356a80e08e7345b12bc9bf5eb10e9d787b478f5ebb3",
                "gpk2": "0x273c3273c072f826f728f865d58ccd297b293b87045fd806973d2a4d82f220a072bc5240c7d5920e0ddfdb0e01aeba184de9ef8ae14f5748243d8fa58d28e136"
            }
    btc = GPK2BTCADDRESS(gr,'main')
    print(btc.public_key_to_address('LTC'))
    print(btc.public_key_to_address('BTC'))
    print(btc.public_key_to_address('DOGE'))
