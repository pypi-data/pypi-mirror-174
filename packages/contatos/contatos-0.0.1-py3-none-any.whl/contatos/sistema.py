from models.conexao import Conexao
from models.contato import Contato
from models.pessoa import Pessoa


def exibir():
    msg = '''
    MENU
    1 - Pesquisar um Contato
    2 - Cadastrar um Contato
    3 - Atualizar um Contato
    4 - Excluir um Contato
    5 - Consultar Todos os Contatos
    6 - Sair do Sistema

    Escolha sua opção (Número entre 1 e 6): '''

    opcao = int(input(msg))

    while (opcao < 1) or (opcao > 6):
        print('\nOpção Inválida.\n')
        opcao = int(input(msg))
    return opcao

def lerNome():
    return input('Digite o nome: ')


def lerTelefone():
    return input('Digite o telefone: ')


def lerEmail():
    return input('Digite o e-mail: ')


def pesquisar(mydb):
    pessoa = Pessoa()
    contato = Contato()
    pessoa.telefone = lerTelefone()
    pessoas = contato.pesquisar(mydb, pessoa)
    if len(pessoas) == 0:
        print('\nContato não cadastrado.')
    else:
        for pessoa in pessoas:
            print(pessoa)


def cadastrar(mydb):
    pessoa = Pessoa()
    contato = Contato()
    pessoa.telefone = lerTelefone()
    pessoas = contato.pesquisar(mydb, pessoa)
    if len(pessoas) == 0:
        pessoa.nome = lerNome()
        pessoa.email = lerEmail()
        contato.cadastrar(mydb, pessoa)
        print('\nContato cadastrado.')
    else:
        print('\nContato já cadastrado.')


def atualizar(mydb):
    pessoa = Pessoa()
    contato = Contato()
    pessoa.telefone = lerTelefone()
    telefone = pessoa.telefone
    pessoas = contato.pesquisar(mydb, pessoa)
    if len(pessoas) == 0:
        print('\nContato não cadastrado.')
    else:
        for p in pessoas:
            pessoa.id = p.id
            pessoa.nome = p.nome
            pessoa.telefone = p.telefone
            pessoa.email = p.email
            print(pessoa)

            pessoa.nome = lerNome()
            pessoa.telefone = lerTelefone()
            pessoa.email = lerEmail()

            contato.atualizar(mydb, telefone, pessoa)
            print('\nContato atualizado.')


def excluir(mydb):
    pessoa = Pessoa()
    contato = Contato()
    pessoa.telefone = lerTelefone()
    pessoas = contato.pesquisar(mydb, pessoa)
    if len(pessoas) == 0:
        print('\nContato não cadastrado.')
    else:
        for p in pessoas:
            contato.excluir(mydb, p)
            print('\nContato excluído.')

def consultarTodos(mydb):
    contato = Contato()
    pessoas = contato.consultar(mydb)
    for p in pessoas:
        print(p)


def executar(opcao, mydb):
    acabou = False
    if opcao == 1:
        pesquisar(mydb)
    elif opcao == 2:
        cadastrar(mydb)
    elif opcao == 3:
        atualizar(mydb)
    elif opcao == 4:
        excluir(mydb)
    elif opcao == 5:
        consultarTodos(mydb)
    else:
        acabou = True
    return acabou
