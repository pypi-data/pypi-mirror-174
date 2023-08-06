import os
import ecdsa
from hashlib import sha256

from ew_crypto_lib.wallets.ew_wallet import Wallet


class FileWallet(Wallet):
    __path:str
    __pk:ecdsa.SigningKey
    __key_slot:int

    def __init__(self, path:str = None) -> None:
        #TODO check path and raise exception
        #os.path.dirname(os.path.abspath(__file__))
        if path is None:
            path = os.path.dirname(os.path.abspath(__file__))
            file_directory = os.path.join(path,'data')
            os.makedirs(file_directory,exist_ok = True)
            path = os.path.join(file_directory, 'private.pem')
        self.__path=path
        with open(path, 'ab+') as f:
            f.seek(0)
            pem = f.read()
            if pem == b'':
                _ = self.generate_key()
                pem = self.__pk.to_pem()
                f.write(pem)
            else:
                self.__pk = ecdsa.SigningKey.from_pem(pem,hashfunc=256)
    
    def set_key_slot(self, slot=0) -> None:
        self.__key_slot = None
    
    def get_public_key(self) -> str:
        if not self.__pk:
            _ = self.generate_key()
        vk:ecdsa.VerifyingKey = self.__pk.verifying_key
        return vk.to_string("uncompressed").hex()

    def generate_key(self) -> str:
        pk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p,hashfunc=sha256)
        self.__pk = pk
        return self.__pk.verifying_key.to_string("uncompressed").hex()

    def sign(self, payload:str) -> bytes:
        hashed = sha256(payload.encode())
        signature = self.__pk.sign_digest(hashed.digest())
        return signature
    
    def verify(self, signature:str, message:str, public_key:str = None) -> bool:
        if public_key is None:
            vk:ecdsa.VerifyingKey = self.__pk.verifying_key
        else:
            vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.NIST256p, hashfunc=sha256)
        try:
            return vk.verify(signature, message)
        except ecdsa.BadSignatureError :
            return False


    @property
    def pk(self) -> str:
        return self.__pk
    @property
    def path(self):
        return self.__path
    @property
    def key_slot(self) -> int:
        return self.__key_slot
    