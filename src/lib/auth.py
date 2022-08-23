import random
import string

from typing import Union
from rsa import encrypt, decrypt, PrivateKey, PublicKey
from src.lib.email_connection import create_email, send_email
from src.lib.db_acess import DatabaseAccess
from datetime import datetime

class Authenticator:
    def __init__(self, db_data) -> None:

        with open("./src/keys/privateKey.pem", "rb") as p:
            self.private_key = PrivateKey.load_pkcs1(p.read())

        with open("./src/keys/publicKey.pem", "rb") as p:
            self.public_key = PublicKey.load_pkcs1(p.read())

        self.all_characters: str = string.ascii_letters + string.digits + string.punctuation
        self.characters: str = string.ascii_letters + string.digits 
        self.db_acess: DatabaseAccess = DatabaseAccess(db_data)
        self.access_level: int = 0

    def __encrypt(self, message: str) -> bytes:
        return encrypt(message.encode(), self.public_key)

    def __decrypt(self, ciphertext: bytes) -> str:
        try:
            return decrypt(ciphertext, self.private_key).decode()
        except:
            return ""

    def validate_login(self, login: str, pwd: str) -> bool:
        #search: list = self.db_acess.search_login(login)
        #search_login: str = search[0]
        #search_pwd: bytes = search[1]
        #self.access_level: int = search[2]

        self.access_level = 0
        search_login = "123456789"
        search_pwd = b'\x8f\x9cY\xce\x85\x0f9\xdc\xdd@V\x88\x7f(>h\x17\xc5\xd6\xae\xd6\x0e"\x8az\x15\xfb\x93\xf31\x94\xaa\x80\xe1\x87d+\x16A\xc5\x9b\xd0F\x97~\xe7\x1b\xff\xf3\x19\xe4U\xa1G\xae\x898\x83\x94\xd8\x81\xcc^\xef>b\xbaY\xfb\x8dO\xc06\xc2O\xdaxM\xd8\'\xe05q\x10W\x8d\xc6\xb6\x0e\xbd\xcc-6\xd5\xc7\x07E\xc2w\xab\x00\xc1!U;_\xca\x05wK\xbd\xb15\r-q\xb4:\xc9\x9a\xcb\x99]g\xef\x0c7j\xd92\x1d\xa0\x17\x11\xe4\xd2\xf1*\xde(G\x87\xc9\x1ay\x14\xe2]\x05\x15\x91%\x18\n|M\x89\x0fWy<p\x11\xa7\x84:\xdd\xc7\xa2+\x1c\xaf\xbdj\x0bR\xab\xc1\xabGP\xaf%AP\x91\x97\xe3\x07W\\\xf2\x00O\x12S\x19\xb5\xb6\xf8u\xfcH\xb7H\xf6\x07\x95s\xdfv\xb5\xa177j\t\x1eC\x0ez\xc5\x0c:\xd7\x8f\xa3\xde\xd1\xed\x90(\xdb\x81: \xb7W {\x7f\x10\xd7\xec\x83\xfd\xfcvl\r\xf9:\xc5\x0e\x05}'

        if search_login == login and pwd == self.__decrypt(search_pwd):
            return True
        else:
            return False   

    def signin_user(self, cpf: str, email: str, pwd: str) -> bool:

        encrypt_pwd: str = self.__encrypt(pwd)

        print(encrypt_pwd)
        
        #return self.db_acess.sign_in_user(cpf, email, encrypt_pwd)

        return True

    def reset_password(self, cpf: str, login: str) -> str:
        
        # get random password pf length 8 with letters, digits, and symbols
        
        password = ''.join(random.choice(self.all_characters) for i in range(8))        
        email = create_email(login, 
                            "Reinicio de senha", 
                            "<strong>Olá,</strong> <br><br> Foi solicitada um reinicio de senha para o seu cadastro.<br> Estou lhe enviando uma senha temporária para uso. <br>SENHA: {}".format(password))
        print(email)
        #self.db_access.change_password(cpf, login, password)
        #send_email()
        return True

    def generate_token(self) -> Union[str, dict]:
        bearer: str = 'Bearer ' + ''.join(random.choice(self.characters) for i in range(1024))
        data = {
            "login_time": datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"),
            "access_level": self.access_level
        }
        return bearer, data
