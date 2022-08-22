import pandas as pd
import mysql.connector

class DatabaseAccess:
    def __init__(self, database_acess: tuple) -> None:
        self.db_access = database_acess

    def search_login(self, login: str) -> list:
        query : str = ("CALL CargosAtuais({});".format(login))
        
        try:
            with mysql.connector.connect(host = self.db_access[0], user = self.db_access[1], password = self.db_access[2]) as connection:
                df = pd.read_sql(query, connection)
        except Exception as e:
            raise Exception("Falha ao se conectar com o banco de dados." + str(e.args))

        return df.values.tolist()[0]

    def sign_in_user(self, cpf: str, email: str, pwd: str) -> bool:
        query : str = ("CALL CargosAtuais({});".format(cpf))
        
        try:
            with mysql.connector.connect(host = self.db_access[0], user = self.db_access[1], password = self.db_access[2]) as connection:
                df = pd.read_sql(query, connection)
        except Exception as e:
            return False

        return True

    def change_password(self, cpf: str, login: str, pwd: str) -> bool:
        query : str = ("CALL CargosAtuais({});".format(cpf, login, pwd))
        
        try:
            with mysql.connector.connect(host = self.db_access[0], user = self.db_access[1], password = self.db_access[2]) as connection:
                df = pd.read_sql(query, connection)
        except Exception as e:
            return False

        return True