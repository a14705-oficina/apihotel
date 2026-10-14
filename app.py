from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

hoteis = [
    {"hotel_id": "paraiso", "nome": "Hotel Paraiso", "Estrelas": 4.8, "Diaria": 125.25, "Cidade": "Porto"},
    {"hotel_id": "bahamas", "nome": "Hotel Bahamas", "Estrelas": 4.7, "Diaria": 110.10, "Cidade": "Vila Real"},
    {"hotel_id": "saint", "nome": "Resort Saint", "Estrelas": 4.3, "Diaria": 143.25, "Cidade": "Lisboa"}
]

class Hoteis(Resource):
    def get(self):
        return {"hoteis": hoteis}


class Hotel(Resource):
    def get(self, hotel_id):
        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return hotel
        return{"mensagem":"Hotel não foi encontrado."}

    def post(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("nome",type=str, required=True, help="O nome do hotel é obrigatório")
        argumentos.add_argument("estrelas",type=float, required=True, help="As estrelas do hotel são obrigatórias")
        argumentos.add_argument("diaria",type=float, required=True, help="A diária do hotel é obrigatório")
        argumentos.add_argument("cidade",type=str, required=True, help="A cidade onde o hotel situa-se é obrigatório")
        dados = argumentos.parse_args() #dados é um dicionário

        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                return { "mensagem": f"O hotel com id {hotel_id} já existe."}
                    
        novo_hotel = {"hotel_id": hotel_id, **dados}
        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatório")
        argumentos.add_argument("estrelas", type=float, required=True, help="As estrelas do hotel são obrigatórias")
        argumentos.add_argument("diaria", type=float, required=True, help="A diária do hotel é obrigatória")
        argumentos.add_argument("cidade", type=str, required=True, help="A cidade onde o hotel se situa é obrigatória")
        dados = argumentos.parse_args() #dados é um dicionário

        for hotel in hoteis:
            if hotel["hotel_id"] == hotel_id:
                hotel.update(dados)
                return hotel, 200
        novo_hotel = {"hotel_id": hotel_id, **dados}.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 201


    def delete(self,hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel["hotel_id"] != hotel_id]
        return {"mensagem": f"O hotel com id {hotel_id} foi removido com sucesso!"}, 200

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    app.run(debug=True)
