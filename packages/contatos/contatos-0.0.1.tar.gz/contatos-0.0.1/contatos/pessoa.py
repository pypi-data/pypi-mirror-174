class Pessoa:

    def __init__(self):
        self.__id = 0
        self.__nome = ''
        self.__telefone = ''
        self.__email = ''


    @property
    def id(self):
        return self.__id


    @id.setter
    def id(self, id):
        self.__id = id


    @property
    def nome(self):
        return self.__nome


    @nome.setter
    def nome(self, nome):
        self.__nome = nome


    @property
    def telefone(self):
        return self.__telefone


    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone


    @property
    def email(self):
        return self.__email


    @email.setter
    def email(self, email):
        self.__email = email


    def __str__(self):
        return '''\nNome: {}\nTelefone: {}\nE-mail: {}\n'''.format(self.nome, self.telefone, self.email)
