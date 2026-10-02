from flask import Flask
from flask_restful import Resource, Api

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
        return{"mensagem":"HOtel não foi encontrado."}
    def delete(self,hotel_id):
        global hoteis
        hoteis = {hotel for hotel in hoteis if hotel("hotel_id") != hotel_id}

api.add_resource(Hoteis,"/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    app.run(debug=True)
