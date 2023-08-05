from models.conexao import Conexao
from models.pessoa import Pessoa


class Contato:

    def pesquisar(self, mydb, pessoa):
        pessoas = []
        p = Pessoa()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM pessoa WHERE telefone = %s"
        val = (pessoa.telefone,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        for r in myresult:
            p.id, p.nome, p.telefone, p.email = r
            pessoas.append(p)
        return pessoas


    def cadastrar(self, mydb, pessoa):
        mycursor = mydb.cursor()
        sql = "INSERT INTO pessoa(nome, telefone, email) VALUES (%s, %s, %s)"
        val = (pessoa.nome, pessoa.telefone, pessoa.email)
        mycursor.execute(sql, val)
        mydb.commit()


    def consultar(self, mydb):
        pessoas = []
        mycursor = mydb.cursor()
        sql = "SELECT * FROM pessoa"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for r in myresult:
            p = Pessoa()
            p.id, p.nome, p.telefone, p.email = r
            pessoas.append(p)
        return pessoas


    def atualizar(self, mydb, telefone, pessoa):
        mycursor = mydb.cursor()
        sql = "UPDATE pessoa SET nome = %s, telefone = %s, email = %s WHERE telefone = %s"
        val = (pessoa.nome, pessoa.telefone, pessoa.email, telefone)
        mycursor.execute(sql, val)
        mydb.commit()


    def excluir(self, mydb, pessoa):
        mycursor = mydb.cursor()
        sql = "DELETE FROM pessoa WHERE telefone = %s"
        val = (pessoa.telefone,)
        mycursor.execute(sql, val)
        mydb.commit()



