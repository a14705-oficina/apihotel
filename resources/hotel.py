from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {"hotel_id":"paraiso","nome":"Hotel Paraiso","estrelas": 4.8,"diaria":125.75,"cidade":"Porto"},
    {"hotel_id":"fukui","nome":"Hotel Fukui Paradise","estrelas": 4.9,"diaria":225.75,"cidade":"Lisboa"},
    {"hotel_id":"saint","nome":"Resort Saint","estrelas": 4.3,"diaria":165.75,"cidade":"Coimbra"}
]

class Hoteis(Resource):
    def get(self):
        return { "hoteis": [hotel.json() for hotel in HotelModel.query.all()] }

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="O nome do hotel é obrigatório")
    argumentos.add_argument("estrelas", type=float, required=True, help="Estrelas é obrigatório")
    argumentos.add_argument("diaria", type=float, required=True, help="Diária é obrigatório")
    argumentos.add_argument("cidade", type=str, required=True, help="Cidade do hotel é obrigatório")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            return hotel.json(), 200
        return { "mensagem": "Hotel não foi encontrado"}

    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args() # dados é um dicionário
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:  
            return { "mensagem": f"O hotel com id {hotel_id} já existe na minha lista."}
        
        novo_hotel = HotelModel(hotel_id, **dados)
        try:
            novo_hotel.save_hotel()
            return novo_hotel.json(), 200   
        except:
            return {"mensagem":"Um erro interno do servidor "}
    
    # Atualizar um hotel
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args() # dados é um dicionário

        # Se o hotel_id existe
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:  
            try:
                hotel.update_hotel(*dados)
                hotel.save_hotel()
                return hotel.json(), 200
        
        # Se o hotel_id não  existe, crie o hotel
        novo_hotel = HotelModel(hotel_id, **dados)
        novo_hotel.save_hotel()
        return novo_hotel.json(), 201
    
    def delete(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is not None:
            hotel.delete_hotel()
            return {"mensagem": "Hotel removido com sucesso"}, 200
        return {"mensagem":"Hotel não encontrado"}, 404
  