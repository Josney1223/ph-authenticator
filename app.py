import os

from flask import Flask, request, Response, session
from flask_cors import cross_origin, CORS
from flask_restful import Resource, Api
from flask_session import Session

from src.validation import validate_json
from src.lib import auth

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
api = Api(app)
Session(app)
#CORS(api)

UPLOAD_FOLDER = os.getcwd()

BD_PASSWORD: str = "B@tat@123"
BD_HOST: str = "10.147.17.25"    
BD_USER: str = "admin"

BD_DATA = [BD_HOST, BD_USER, BD_PASSWORD]

# Isso é horrível, mas nn tenho tempo pra consertar...
SERVER: str = "10.147.17.25" #"192.168.66.102"#
API_ENDPOINT_EXCEL: str = "http://"+SERVER+":2001/api/v1/GerarExcel/ExcelEmpresa"
API_ENDPOINT_EMAIL: str = "http://"+SERVER+":2002/api/v1/GerarEmail/EmailBasico"
API_ENDPOINT_PDF: str = "http://"+SERVER+":2003/api/v1/GerarPDF/FromJson"
API_ENDPOINT_ZIP: str = "http://"+SERVER+":2000/api/v1/GerarZip/AES"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class GerarFDP(Resource):

    @app.route("/api/v1/Auth/UserAuth", methods=["GET"])       
    def UserAuth(*self):
        request_json = request.get_json()

        if not validate_json.validator(request_json, "login"):
            return Response("Json invalido", status=400)

        worker: auth.Authenticator = auth.Authenticator(BD_DATA)

        if not worker.validate_login(request_json["username"], request_json["password"]):
            return Response("Forbidden", status=403)

        token, data = worker.generate_token() 
               
        session[token] = data

        return Response("Autenticado", status=200)

    @app.route("/api/v1/Auth/UserSignin", methods=["POST"])       
    def UserSignin(*self):
        request_json = request.get_json()

        if not validate_json.validator(request_json, "signin"):
            return Response("json invalido", status=400)

        worker: auth.Authenticator = auth.Authenticator(BD_DATA)

        if not worker.signin_user(request_json["cpf"], request_json["email"], request_json["password"]):
            return Response("Server Error", status=500)

        return Response("Autenticado", status=202)

    @app.route("/api/v1/Auth/ResetPassword", methods=["GET"])       
    def ResetPassword(*self):
        request_json = request.get_json()

        if not validate_json.validator(request_json, "reset_pwd"):
            return Response("json invalido", status=400)

        worker: auth.Authenticator = auth.Authenticator(BD_DATA)

        if not worker.reset_password(request_json["cpf"], request_json["email"]):
            return Response("Server Error", status=500)

        return Response("Email Reenviado", status=200)

    @app.route("/api/v1/Auth/ValidateToken", methods=["GET"])       
    def ValidateToken(*self):
        args = request.args

        if not args["Authorization"]:
            return Response("token não enviado", status=400)
        elif not session.get(args["Authorization"]):
            return Response("Usuário não logado", status=401)                

        return Response("Autorizado", status=200)
    

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=2000)