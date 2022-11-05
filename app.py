import os

from json import dumps

from flask import Flask, request, Response, session
from flask_cors import cross_origin, CORS
from flask_restful import Resource, Api
from flask_session import Session

from src.validation import validate_json
from src.lib import auth

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'CDgWUjqcCaNURJD9AkcRgKaTucApXBGH'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'

api = Api(app)
Session(app)

class PHAuth(Resource):

    @app.route("/api/v1/Auth/UserAuth", methods=["POST"])       
    def UserAuth(*self):
        request_json = request.get_json()

        if not validate_json.validator(request_json, "login"):
            return Response(dumps(validate_json.get_json_schema("login")), status=400, mimetype='application/json')

        worker: auth.Authenticator = auth.Authenticator()

        if not worker.validate_login(request_json["username"], request_json["password"]):
            return Response("Forbidden", status=403)

        token, data = worker.generate_token() 
               
        session[token] = data

        return Response("Autenticado", status=200, headers={"access_token": token})

    @app.route("/api/v1/Auth/UserSignin", methods=["POST"])       
    def UserSignin(*self):
        request_json = request.get_json()

        if not validate_json.validator(request_json, "signin"):
            return Response(dumps(validate_json.get_json_schema("signin")), status=400, mimetype='application/json')

        worker: auth.Authenticator = auth.Authenticator()

        return worker.signin_user(request_json["cpf"], request_json["cnpj"], request_json["email"], request_json["nome_completo"], request_json["password"])                    

    @app.route("/api/v1/Auth/ResetPassword", methods=["POST"])       
    def ResetPassword(*self):
        request_json = request.get_json()

        if not validate_json.validator(request_json, "reset_pwd"):
            return Response(dumps(validate_json.get_json_schema("reset_pwd")), status=400, mimetype='application/json')

        worker: auth.Authenticator = auth.Authenticator()

        if not worker.reset_password(request_json["cpf"], request_json["cnpj"], request_json["email"]):
            return Response("Server Error", status=500)

        return Response("Email Enviado", status=200)

    @app.route("/api/v1/Auth/ValidateToken", methods=["GET"])       
    def ValidateToken(*self):
        args = request.headers

        if not args["Authorization"]:
            return Response("token não enviado", status=400)
        elif not session.get(args["Authorization"]):
            return Response("Usuário não logado", status=401)                

        return Response("Autorizado", status=200)
    

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=2000)