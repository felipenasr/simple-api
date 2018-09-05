from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from pymongo import MongoClient
from json import dumps
from bson.json_util import dumps
import datetime

client = MongoClient('localhost', 27017)
db = client.db_blog
app = Flask(__name__)
api = Api(app)

publicacoes = db.col_publicacoes

class Response():
    def RetornoConsulta(data, statusCode):
        response = jsonify({"data": data})
        response.status_code = statusCode
        return response
    def RetornoInsercao(sucesso):
        response = jsonify({"sucesso": sucesso})
        if sucesso:
            response.status_code = 200
        else:
            response.status_code = 400
        return response
        
class ConsultarPublicacoes(Resource):
    def get(self):
        listarTodas = dumps(publicacoes.find())        
        return Response.RetornoConsulta(listarTodas, 200)


class InserirPublicacao(Resource):
    def post(self):
        publicacao = {}
        publicacao['titulo'] = request.json['titulo']
        publicacao['subtitulo'] = request.json['subtitulo']
        publicacao['texto'] = request.json['texto']
        publicacao['autor'] = request.json['autor']
        publicacao['url'] = request.json['url']
        publicacoes.insert_one(publicacao)
        return Response.RetornoInsercao(True)


api.add_resource(ConsultarPublicacoes, '/api/listar-todos')
api.add_resource(InserirPublicacao, '/api/novo-post')

if __name__ == "__main__":
    app.run()