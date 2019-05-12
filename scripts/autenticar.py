import btree 
import rfid

f = open("mydb", "r+b")     #abre o arquivo de banco de dados "mydb"

db = btree.open(f)

def aut():       #funçao responsável pela autenticação do cartão
    while True:
        print("Aguartando o cartao para autenticar..")
        codCartao = (rfid.Mfrc522().read())  #Faz a leitura do cartao pelo script do rfid.py
        print (codCartao)
        for i in db:
            if codCartao == db[i].decode():    #varre o banco de dados(1 à 1), comparando com o cartao lido
                return True
            else:
                pass     
        return False 

    db.close()     #fecha o banco de dados 
    f.close()