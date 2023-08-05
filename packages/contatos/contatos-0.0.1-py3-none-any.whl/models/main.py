from models.conexao import Conexao
from models.sistema import *


def main():
    conexao = Conexao('contato', 'root', 'root')
    mydb = conexao.conectar()
    acabou = False
    while not acabou:
        opcao = exibir()
        acabou = executar(opcao, mydb)


if __name__ == '__main__':
    main()