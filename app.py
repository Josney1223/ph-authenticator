import os

from json import dumps

from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_session import Session

from src.lib.cors import build_cors_preflight_response, build_cors_response
from src.validation import validate_json
from src.lib import auth

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__)

api = Api(app)
Session(app)

class PHAuth(Resource):

    @app.route("/api/v1/Auth/UserAuth", methods=["POST"])       
    def UserAuth(*self):
        if request.method == "OPTIONS": return build_cors_preflight_response()
        request_json = request.get_json()

        if not validate_json.validator(request_json, "login"):
            return Response(dumps(validate_json.get_json_schema("login")), status=400, mimetype='application/json')

        worker: auth.Authenticator = auth.Authenticator()        

        return worker.login_complete(request_json['email'], request_json['password'])

    @app.route("/api/v1/Auth/UserSignin", methods=["POST"])       
    def UserSignin(*self):
        if request.method == "OPTIONS": return build_cors_preflight_response()
        request_json = request.get_json()

        if not validate_json.validator(request_json, "signin"):
            return Response(dumps(validate_json.get_json_schema("signin")), status=400, mimetype='application/json')

        worker: auth.Authenticator = auth.Authenticator()

        return worker.signin_user(request_json["cpf"], 
                                request_json["cnpj"],
                                request_json["email"],
                                request_json["nome_usuario"],
                                request_json["password"])

    @app.route("/api/v1/Auth/ResetPassword", methods=["POST"])       
    def ResetPassword(*self):
        if request.method == "OPTIONS": return build_cors_preflight_response()
        request_json = request.get_json()

        if not validate_json.validator(request_json, "reset_pwd"):
            return Response(dumps(validate_json.get_json_schema("reset_pwd")), status=400, mimetype='application/json')

        worker: auth.Authenticator = auth.Authenticator()

        return worker.reset_password(request_json["cpf"], request_json["cnpj"], request_json["email"])                    

    @app.route("/api/v1/Auth/ValidateToken", methods=["GET"])       
    def ValidateToken(*self):        
        header = request.headers        
        
        if "Access-Token" not in header.keys(): 
            return Response("Token não enviado", status=400)

        worker: auth.Authenticator = auth.Authenticator()
        
        return worker.validate_token(header["Access-Token"])
    
    @app.after_request
    def AfterRequest(response: Response):
        return build_cors_response(response)


if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=2000)
