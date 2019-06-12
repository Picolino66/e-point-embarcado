import gc
import btree
gc.collect()
import ujson
gc.collect()
import utime
gc.collect()

from config import (
    LOG_TABLE,
    MEMBER_TABLE,
    P_SIZE,
    MEMBER_SOURCE,
    LOG_SOURCE
)
gc.collect()

class Udb():
    """ Classe base para armazenamento e manipulação do módulo `btree` """
    def __init__(self, filename):
        self.filename = filename
        f, db = self.open(1)
        self.close(f, db)

    def open(self, _init=False):
        """ Método para abrir o arquivo e retornar um objeto `File` do arquivo aberto e um `btree`

        :param init: Flag que indica se o método deve criar um arquivo caso não esteja criado
        :type init: Boolean

        Caso seja criado um novo arquivo, é usada a primeira posição da `btree`
        """

        try:
            f = open(self.filename, "r+b")
            db = btree.open(f, pagesize=P_SIZE)
        except OSError:
            if _init:
                f = open(self.filename, "w+b")
                db = btree.open(f, pagesize=P_SIZE)
                # Primeira posição é um cabeçalho que indica a quantidade de elementos
                db[bytes([0])] = bytes([1])
            else:
                print("DB não foi inicializado")
                return False
        return f, db

    def close(self, f, db):
        """ Método para fechar o arquivo e limpar o fluxo"""
        db.flush()
        db.close()
        f.close()

    def list(self):
        """ Método para listar cada par key/value do banco de dados """
        f, db = self.open()
        for key in db:
            print(key + ": " + db[key])
        self.close(f, db)

    def insertJson(self, json):
        f, db = self.open()
        header = db[bytes([0])]
        try:
            db[header] = bytes(ujson.dumps(json), 'utf8')
            db[bytes([0])] = bytes([int.from_bytes(header, 'little')+1])
        except OSError:
            print("Disco cheio")
        self.close(f, db)

    def update(self, key, value):
        """ Método que atualiza um value (json) do banco de dados
        :param key: Chave do registro 
        :param value: Valor (json) a ser inserido
        """
        f, db = self.open()
        # TODO: reescrever apenas um value, não o json inteiro
        db[key] = bytes(ujson.dumps(value), 'utf8')
        self.close(f, db)

    def select(self, all=False, **kwargs):
        r""" Retorna o value de um registro que possua contenha campos específicos passados em `kwargs`.
        Caso contrário, retorna None.
        :param all: 
            Indica se o método retornará apenas o primeiro registro, ou uma lista com todos.
        :param \**kwargs:
            Parâmetros da model

        """
        query_resp = []
        key_resp = []
        if kwargs:
            f, db = self.open()
            for key in list(db.keys())[::-1]:
                try: 
                    query = ujson.loads(db[key])
                    match = 1
                    for parameter, value in kwargs.items():
                        if not query[parameter] == value:
                           match = 0 
                           break
                        elif all:
                            query_resp.append(query)
                            key_resp.append(key)
                    if match and not all:
                        self.close(f, db)
                        return query, key
                except ValueError:
                    # última posição do banco (cabeçalho)
                    pass
            self.close(f, db)

        return query_resp, key_resp

    def get_pendings(self):
        return self.select(all=True, sent=False)

class Member(Udb):
    """ Classe, filha de `Udb`, que gerencia a "tabela" de membros no banco de dados.
        Campos:
        - id: identificador do cartão 
        - name: Nome do usuário (membro)
        - email: Email do usuário (membro)
        - present: Estado do usuário. 0 se fora da sala e 1 se cumprindo horário
        - time: Horário do cadastro
    """
    def __init__(self):
        super(Member, self).__init__(MEMBER_TABLE)
        self.source = MEMBER_SOURCE

    def count_presents(self):
        """ """
        f, db = self.open()
        count = 0
        for key in list(db.keys()):
            try: 
                query = ujson.loads(db[key])
                if query["present"]:
                    count += 1
            except ValueError:
                # última posição do banco (cabeçalho)
                pass
        self.close(f, db)
        return count

    def new_transaction(self, id, name, email, present=0, sent=0, time=utime.localtime()):
        """ Método para inserir um novo registro na "tabela" `member` """
        query, key = self.select(id=id)
        if not query:
            json = {}
            json['id'] = id
            json['name'] = name
            json['email'] = email
            json['present'] = present
            json['sent'] = sent
            json['time'] = time
            self.insertJson(json) 
            return json

        return False
        
    def clean_status(self):
        """ Método para limpar os status dos membros """
        f, db = self.open()
        count = 0
        for key in list(db.keys()):
            try: 
                query = ujson.loads(db[key])
                print(query['present'])
                query['present'] = False
                self.update(key, query)
                print(query['present']) 
            except ValueError:
                # última posição do banco (cabeçalho)
                pass
        self.close(f, db)

class Log(Udb):
    """ Classe, filha de `Udb`, que gerencia a "tabela" de Log no banco de dados.
        Campos:
        - id: identificador do cartão 
        - type: Identificador de entrada ou saída (1 para entrada e 0 para saída) (membro)
        - sent: Identificador de envio para servidor (0 se não foi enviado e 1 caso contrário) 
        - time: Horário do cadastro
        - create_json: Adicionado um campo que indica se o log deixou a sala vazia
    """
    def __init__(self, member):
        self.member = member
        super(Log, self).__init__(LOG_TABLE)
        self.source = LOG_SOURCE

    def new_transaction(self, id, sent=0, time=utime.localtime()):
        """ Método para inserir um novo registro na "tabela" `log`"""
        query, key = self.member.select(id=id)
        def create_json(left_empty = 0):
            query["present"] = not query["present"]
            self.member.update(key, query)
            json = {}
            json['id'] = id
            json['type'] = 1 if query["present"] else 0
            json['sent'] = sent
            json['time'] = time
            json['left_empty'] = left_empty
            return json
        if not query:
            print("query vazia")
            return False, False, False
        # sala irá ficar vazia
        elif query["present"] and self.member.count_presents() == 1:
            print("sala vazia")
            json = create_json(1)
            self.insertJson(json)
            return False, True, False
        # sala já possui 5 pessoas
        elif not query["present"] and self.member.count_presents() >= 5:
            print("sala cheia")
            return False, False, True
        json = create_json()
        self.insertJson(json) 
        return json, False, False
