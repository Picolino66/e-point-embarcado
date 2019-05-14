import btree
import ujson
import rfid

def cadastrar():

    try:                               #tenta abrir um arquivo "mydb", se nao encontrar, cria-se um.
        f = open("mydb", "r+b")
    except OSError:
        f = open("mydb", "w+b")

    db = btree.open(f)

    def adicionar(matricula, codCartao):        #Funçao que realiza o cadastro no banco de dados
        db[matricula] = codCartao
        db.flush
    
    def deletar(matricula):            #Funçao para deletar alguma key do banco de dados
        del db[matricula]
        db.flush()

    while True:
        print("Para adicionar, digite 1")
        print("Para deletar, digite 2")
        print("Para listar, digite 3")
        print("Para sair e salvar, digite 4")

        modo = input("modo: ")      
    
        if modo == '1':
            matricula = input("matricula: ")
            codCartao = rfid.Mfrc522().read() #Faz a leitura do cartao pelo script do rfid.py
            adicionar(matricula, codCartao) 
        elif(modo == '2'):
            matricula = input("Digite a key da matricula a ser deletada: ")
            deletar(matricula)
        elif(modo == '3'):
            print("Printando..................")
            for i in db:
                print(i, "---", db[i])
        else:
            db.close()
            f.close()
            break