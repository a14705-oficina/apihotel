from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):

    def get(self,username):
        user = UserModel.find_user(username) # Devolve o utilizador encontrado ou devolve None
        if user is not None:
            return user.json(), 200
        return { "mensagem": "Utilizador não foi encontrado"}

    
    def delete(self,username):
        user = UserModel.find_user(username)
        if user is not None:
            user.delete_hotel()
            return {"mensagem": "Utilizador removido com sucesso"}, 200
        return {"mensagem":"Utilizador não encontrado"}, 404


class UserRegister(Resource):
        argumentos = reqparse.RequestParser()
        argumentos.add_argument("username", type=str, required=True, help="O nome do Utilizador é obrigatório")
        argumentos.add_argument("password", type=float, required=True, help="Password obrigatória")

    def post(self):
        dados = UserRegister.argumentos.parse_args()
        if UserModel.find_user(dados["username"]):
            return {"mensagem":"Já existe um utilizador com este username."}, 400
        novo_utilizador = UserModel(**dados)
        try:
             novo_utilizador.save_user()
             return {"mensagem": "Utilizador criado com sucesso"}, 200
        except:
            return {"mensagem": "Erro interno ocorreu..."}, 500
