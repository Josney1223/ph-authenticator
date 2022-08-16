import os
import requests
import uuid

from flask import Flask, request, Response
from flask_cors import cross_origin, CORS
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
CORS(api)

UPLOAD_FOLDER = os.getcwd()

BD_PASSWORD: str = "B@tat@123"
BD_HOST: str = "10.147.17.25"    
BD_USER: str = "admin"

# Isso é horrível, mas nn tenho tempo pra consertar...
SERVER: str = "10.147.17.25" #"192.168.66.102"#
API_ENDPOINT_EXCEL: str = "http://"+SERVER+":2001/api/v1/GerarExcel/ExcelEmpresa"
API_ENDPOINT_EMAIL: str = "http://"+SERVER+":2002/api/v1/GerarEmail/EmailBasico"
API_ENDPOINT_PDF: str = "http://"+SERVER+":2003/api/v1/GerarPDF/FromJson"
API_ENDPOINT_ZIP: str = "http://"+SERVER+":2000/api/v1/GerarZip/AES"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class GerarFDP(Resource):

    @app.route("/api/v1/Auth/UserAuth", methods=["GET"]) 
    @cross_origin()   
    def gerar_fdp(*self):
        response_json = request.args

    
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=2000)