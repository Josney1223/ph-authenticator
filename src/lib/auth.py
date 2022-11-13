import random
import string
import pandas as pd
import mysql.connector
import os

from flask import Response
from mysql.connector.errors import IntegrityError, DatabaseError
from sqlalchemy import create_engine, engine
from typing import Union
from rsa import encrypt, decrypt, PrivateKey, PublicKey
from src.lib.email_connection import create_email, send_email
from json import dumps


class Authenticator:
    def __init__(self) -> None:

        path: str = os.getcwd()
        
        with open(os.path.join(path, "src", "keys", "privateKey.pem"), "rb") as p:
            self.private_key = PrivateKey.load_pkcs1(p.read())

        with open(os.path.join(path, "src", "keys", "publicKey.pem"), "rb") as p:
            self.public_key = PublicKey.load_pkcs1(p.read())

        self.db_access: tuple[str] = ("10.147.17.25", "admin_projeto_horizonte", "PROJETO TI@TCC2022") 
        self.db_engine: engine.Engine = create_engine('mysql+pymysql://admin_projeto_horizonte:PROJETO%20TI%40TCC2022@10.147.17.25:3306/ProjetoHorizonte')
        self.all_characters: str = string.ascii_letters + string.digits              
        self.access_level: int = 0

    def __run_query(self, query: str, params: tuple = (), has_return: bool = True) -> Union[pd.DataFrame, None]:
        
        if has_return:
            try:   
                df = pd.read_sql(query, con=self.db_engine)         
                return df
            except Exception as e:
                raise Exception("Falha ao se conectar com o banco de dados.", e.args)        
        else:
            with mysql.connector.connect(host = self.db_access[0],                                                
                                        user = self.db_access[1],
                                        password = self.db_access[2]) as con:
                cursor = con.cursor()
                cursor.execute(query, params)
                con.commit()

        return None

    def __encrypt(self, message: str) -> bytes:
        return encrypt(message.encode(), self.public_key)

    def __decrypt(self, ciphertext: bytes) -> str:
        try:
            return decrypt(ciphertext, self.private_key).decode()
        except:
            return ""

    def _validate_login(self, login: str, pwd: str) -> bool:
        query: str = "CALL ProjetoHorizonte.BuscaSenha('{}');".format(login)    

        # Busca Senha ----------

        try:                               
            search_pwd = self.__run_query(query).values.tolist()[0][0]
        except Exception as ex:
            return False
        
        # Validar Senha ----------        

        if pwd == self.__decrypt(search_pwd):
            return True
        else:
            return False  

    def _generate_token(self, login: str) -> str:
        
        new_bearer: str = ''.join(random.choice(self.all_characters) for i in range(1024))
        query: str = "CALL ProjetoHorizonte.RealizarAcessoToken('{}', '{}');".format(login, new_bearer)        

        try:
            bearer: str = 'Bearer {}'.format(self.__run_query(query).values.tolist()[0][0])
        except Exception as ex:
            print(ex.args)
            
        return bearer

    def _get_access_level(self, login: str) -> int:
        query: str = "CALL ProjetoHorizonte.BuscaNivelAcesso('{}');".format(login)                        
        return int(self.__run_query(query).values.tolist()[0][0])

    def login_complete(self, login: str, pwd: str) -> Response:
        
        dict_response: dict = {}

        if not self._validate_login(login, pwd): return Response("Forbidden", status=403)  

        dict_response["access_level"] = self._get_access_level(login)
        dict_response["access_token"] = self._generate_token(login)

        return Response(dumps(dict_response), 200)

    def signin_user(self, cpf: str, cnpj: str, email: str, nome_completo: str, pwd: str) -> Response:
        encrypt_pwd: bytes = self.__encrypt(pwd)

        if cnpj == "00000000000000" and cpf == "000000000": return False

        cnpj_value: Union[str, None] = None if cnpj == "00000000000000" else cnpj
        cpf_value: Union[str, None] = None if cpf == "00000000000000" else cpf

        query: str = "CALL ProjetoHorizonte.CadastrarUsuario(%s, %s, %s, %s, %s);"
        params: tuple = (cpf_value, cnpj_value, email, nome_completo, encrypt_pwd)
        
        try:
            self.__run_query(query, params=params, has_return=False)
        except IntegrityError as ie:
            print(ie.args)
            return Response("Usuário já cadastrado", status=409)

        return Response("Autenticado", status=202)

    def reset_password(self, cpf: str, cnpj: str, login: str) -> Response:
        
        if cnpj == "00000000000000" and cpf == "000000000": return False

        cnpj_value: Union[str, None] = None if cnpj == "00000000000000" else cnpj
        cpf_value: Union[str, None] = None if cpf == "00000000000000" else cpf

        password = ''.join(random.choice(self.all_characters) for i in range(8)) 
        query: str = "CALL ProjetoHorizonte.AlterarSenha(%s, %s, %s, %s);"
        params: tuple = (cpf_value, cnpj_value, login, self.__encrypt(password))

        try:
            self.__run_query(query, params=params, has_return=False)
        except DatabaseError as ie:
            return Response("Usuário não cadastrado.", status=404)

        email = create_email([login], 
                            "Reinicio de senha", 
                            "<strong>Olá,</strong> <br><br> Foi solicitada um reinicio de senha para o seu cadastro.<br> Estou lhe enviando uma senha temporária para uso. <br>SENHA: {}".format(password))
        send_email(email)

        return Response("E-mail enviado", status=200)

    def validate_token(self, token: str) -> Response:
        
        query: str = "CALL ProjetoHorizonte.ValidarToken('{}');".format(token[7:])

        try:
            id_user: int = self.__run_query(query).values.tolist()[0][0]            
        except Exception as ex:            
            if ex.args[1][0] == "(pymysql.err.OperationalError) (1644, 'Token Inexistente')":               
                return Response("Token inválido", 401)
            elif ex.args[1][0] == "(pymysql.err.OperationalError) (1644, 'Token Expirado')":
                return Response("Token Expirado", 401)

        return Response(dumps({"id_user": id_user}), 200, mimetype="application/json")
