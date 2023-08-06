from xrpl.core.keypairs import derive_classic_address
from coincurve import PublicKey

class GPK2XRPADDRESS:
    '''
    '''
    def get_sm_xrp_address(self, gpk_curve:dict):
        '''
        {
            "curve1": "1",
            "curve2": "0",
            "gpk1": "0x0c440bf2b594bdf526cbbcaae75dcb5f93d1f9bdd2f234f853fe4acf5f0e2d6d0525ad07f29f86943bc7c356a80e08e7345b12bc9bf5eb10e9d787b478f5ebb3",
            "gpk2": "0x273c3273c072f826f728f865d58ccd297b293b87045fd806973d2a4d82f220a072bc5240c7d5920e0ddfdb0e01aeba184de9ef8ae14f5748243d8fa58d28e136"
        }
        '''
        if gpk_curve['curve1'] == 0:
            xrp_pk = gpk_curve['gpk1']
        else:
            xrp_pk = gpk_curve['gpk2']
        raw_key = bytes.fromhex('04' + xrp_pk[2::])
        compress_pub = PublicKey(raw_key).format()
        return derive_classic_address(compress_pub.hex())


    def gen_xrp_address(self, pk):
        raw_key = bytes.fromhex('04' + pk[2::])
        compress_pub = PublicKey(raw_key).format()
        return derive_classic_address(compress_pub.hex())

if __name__ == '__main__':
    gr =         {
            "curve1": "1",
            "curve2": "0",
            "gpk1": "0x0c440bf2b594bdf526cbbcaae75dcb5f93d1f9bdd2f234f853fe4acf5f0e2d6d0525ad07f29f86943bc7c356a80e08e7345b12bc9bf5eb10e9d787b478f5ebb3",
            "gpk2": "0x273c3273c072f826f728f865d58ccd297b293b87045fd806973d2a4d82f220a072bc5240c7d5920e0ddfdb0e01aeba184de9ef8ae14f5748243d8fa58d28e136"
        }
    print(GPK2XRPADDRESS().get_sm_xrp_address(gr))
    # print(gen_xrp_address("7251664a3372615355544b6b7a4e35624373425a4e425473733159776b36796f"))