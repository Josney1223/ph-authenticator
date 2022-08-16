from cryptography.fernet import Fernet
from pull_data import DatabaseAccess

KEY = b'PRk2bsnp48XgWk7V4V35Qsd70jufgntZFt6P9R20sEo='

class Authenticator:
    def __init__(self, db_data) -> None:
        self.cipher_suit = Fernet(KEY)
        self.db_acess: DatabaseAccess = DatabaseAccess(db_data)

    def validate_login(self, login: str, pwd: str) -> bool:
        search: list = self.db_acess.search_login(login)
        search_login: str = search[0]
        search_pwd: bytes = search[1]

        if search_login == login and search_pwd == self.cipher_suit.encrypt(pwd):
            return True
        else:
            return False    
