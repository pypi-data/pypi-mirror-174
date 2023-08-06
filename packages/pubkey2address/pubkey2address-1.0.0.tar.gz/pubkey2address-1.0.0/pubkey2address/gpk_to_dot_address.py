import hashlib
from coincurve import PublicKey
from substrateinterface import Keypair

class GPK2DOTADDRESS:
    def get_sm_dot_address(self, gpk_curve:dict,net):
        '''
        :param gpk_curve:
            {
                "curve1": "1",
                "curve2": "0",
                "gpk1": "0x0c440bf2b594bdf526cbbcaae75dcb5f93d1f9bdd2f234f853fe4acf5f0e2d6d0525ad07f29f86943bc7c356a80e08e7345b12bc9bf5eb10e9d787b478f5ebb3",
                "gpk2": "0x273c3273c072f826f728f865d58ccd297b293b87045fd806973d2a4d82f220a072bc5240c7d5920e0ddfdb0e01aeba184de9ef8ae14f5748243d8fa58d28e136"
            }
        '''
        if net == 'main':
            ss58Format = 0
        else:
            ss58Format = 42
        if gpk_curve['curve1'] == 0:
            dot_pk = gpk_curve['gpk1']
        else:
            dot_pk = gpk_curve['gpk2']

        return self.gen_dot_address_from_gpk(dot_pk,ss58Format)

    def gen_dot_address_from_gpk(self,gpk,ss58Format):
        raw_key = bytes.fromhex('04' + gpk[2::])
        compress_pub = PublicKey(raw_key).format()
        gfg = hashlib.blake2b(digest_size=32)
        gfg.update(compress_pub)
        keypair = Keypair(public_key=gfg.digest(), ss58_format=ss58Format, crypto_type=1)
        return keypair.ss58_address

    def gen_dot_address_from_pubkey(self,pubKey,net):
        '''
        :param pubKey:
        :return:
        '''
        if net == 'main':
            ss58Format = 0
        else:
            ss58Format = 42
        return self.gen_dot_address_from_gpk(pubKey,ss58Format)

if __name__ == '__main__':
    gr =   {
                "curve1": "1",
                "curve2": "0",
                "gpk1": "0x0c440bf2b594bdf526cbbcaae75dcb5f93d1f9bdd2f234f853fe4acf5f0e2d6d0525ad07f29f86943bc7c356a80e08e7345b12bc9bf5eb10e9d787b478f5ebb3",
                "gpk2": "0x273c3273c072f826f728f865d58ccd297b293b87045fd806973d2a4d82f220a072bc5240c7d5920e0ddfdb0e01aeba184de9ef8ae14f5748243d8fa58d28e136"
            }
    dotaaddr = GPK2DOTADDRESS()
    print(dotaaddr.get_sm_dot_address(gr,'test'))

