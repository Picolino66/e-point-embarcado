#Arquivo que controla os Bancos de Dados
import machine
import btree
import ujson
import time

class Banco():
    """Classe mae que controla as principais funcoes de controle do banco de dados"""
    def __init__(self, filename):
        self.filename = filename
        f, db = self.open(1)

    def open(self, _init=False):
        """Funcao responsavel por abrir os banco de dados"""
        try:
            f = open(self.filename, "r+b")
            db = btree.open(f, pagesize = 512)
        except OSError:
            if _init:
                f = open(self.filename, "w+b")
                db = btree.open(f,pagesize = 512)
            else:
                print("DB nao iniciou")
                machine.reset()
        return f, db

    def close(self, f, db):
        """Funcao responsavel por fechar os banco de dados"""
        db.flush()
        db.close()
        f.close()

    def list(self):
        """Funcao responsavel por listar o conteudo dos banco de dados"""
        f, db = self.open()
        for key in db:
            print(key,"-",db[key])
        self.close(f, db)

    def add_json(self,json):
        """Funcao responsavel por adicionar no banco de dados, quando o conteudo for um Json"""
        f, db = self.open()
        cont = 100
        try:
            for key in db:
                cont = cont+1
            proximo = str(cont)
            db[proximo] = ujson.dumps(json)
        except OSError:
            machine.reset()
        self.close(f, db)

class Log(Banco):
    """Classe filha de 'Banco' que controla a autenticacao dos membros"""
    def __init__(self):
        super(Log,self).__init__('log_table')

    def new_log(self, id, entrou = 0,dateTime = [], presente=0, enviado=0):
        """Funcao que adiciona um novo membro na tabela 'log_table'.\n
            Parametros:\n\n
            -'id' (id do cartao);
            -'entrou' (se o membro esta entrando(1) ou saindo(0) da reuniao;
            -'dateTime' (data e hora em que o cartao foi batido)
            -'presente' (se o membro esta ausente(0), no horario(1) ou atrasado(2))
            -'enviado' (registro enviado para servidor(1), nao enviado ainda(0))
        """
        json = {
            "id":id,
            "dateTime": dateTime,
            "entrou":entrou, 
            "presente": presente,
            "enviado": enviado
            }
        self.add_json(json)
        return json
        
    def status_entrou(self, id):
        """Funcao que verifica se o membro esta entrando ou saindo da reuniao.\n
            Parametros:\n
            -'id' (id do cartao);
        """
        entrou = 0
        f, db = self.open()
        try:
            for key in db:
                loads = ujson.loads(db[key])
                if id == loads["id"]:
                    entrou = loads["entrou"]
            return entrou
        except OSError:
            machine.reset()

class Cadastro(Banco):
    """Classe filha de 'Banco' que controla o cadastro dos membros"""
    def __init__(self):
        super(Cadastro,self).__init__('member_table')

    def new_member(self, id, matricula):
        """Funcao que adiciona um novo membro na tabela 'member_table'.\n
            Parametros:\n
            -'id' (id do cartao);
            -'matricula' (matricula do membro).
        """
        f, db = self.open()
        matricula = str(matricula)
        db[matricula] = id
        self.close(f, db)


    def del_member(self, matricula):
        """Funcao que deleta um membro da tabela 'member_table'.\n
            Parametros:\n
            -'matricula' (matricula do membro à ser deletado).
        """
        f, db = self.open()        
        matricula = str(matricula).encode()
        print(matricula," deletado")
        del db[matricula]
        self.close(f, db)