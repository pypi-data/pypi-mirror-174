import mysql.connector


class Conexao:

    def __init__(self, database, user, password):
        self.__database = database
        self.__user = user
        self.__password = password

    def conectar(self):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user=self.__user,
                password=self.__password,
                database=self.__database
                )
            print('Sucesso na conexão com o banco de dados.')
            return mydb
        except:
            print('Sem sucesso na conexão com o banco de dados.')